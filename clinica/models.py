from django.db import models
import datetime

# Create your models here.

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

STAFF_DESIGNATION = (
    ('Doctor', 'Doctor'),
    ('Nurse', 'Nurse'),
    ('Lab Technician', 'Laboratory Technician'),
    ('Receptionist', 'Receptionist'),
)

CLINIC_TYPE = (
    ('IN', 'INPATIENT'),
    ('OUT', 'OUTPATIENT'),
)

FUNCTIONAL_STATUS = (
    ('NEW','NEWLY ACQUIRED'),
    ('GOOD','GOOD WORKING CONDITION'),
    ('REPAIR','DUE FOR SERVICE'),
    ('UNREPAIRABLE','UNREPAIRABLE'),
)

ASSET_INVENTORY = (
    ('MEDICAL','MEDICAL'),
    ('ELECTRO', 'ELECTRO-MECHANICAL'),
    ('FURNITURE','FURNITURE'),
)


class FixedAssetInventory(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    category = models.CharField(max_length=100, choices=ASSET_INVENTORY, verbose_name='category')
    acquired_on = models.DateField(null=False, verbose_name='Equipment Delivery Date')
    service_period = models.PositiveIntegerField(verbose_name='Service Interval')
    last_service_date = models.DateField(verbose_name='Last Service Date', blank=True)
    service_due = models.BooleanField(default=False, verbose_name='Due for Service?')

    def __unicode__(self):

        return u'%s - %s' % (self.name, self.category)

    class Meta:
        verbose_name_plural = 'Fixed Asset Inventory'

    def due_for_service(self):

        """ Calculate when equipment is due for service
        """

        #get today's date

        today = datetime.date.today()

        #Calculate due date for service based on last service date and the service interval

        service_due_date = self.last_service_date + datetime.timedelta(self.service_period)

        # Setting service due boolean field

        if service_due_date > today:
            self.service_due = True








class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    address = models.CharField(max_length=100, verbose_name='address')
    phone = models.CharField(max_length=30, verbose_name='Phone Number')
    alternate_phone = models.CharField(max_length=30, verbose_name='Alternate Phone Number', blank=True)
    email = models.EmailField(max_length=100,verbose_name='Email', blank=True)

    def __unicode__(self):

        return u'%s' % self.name

    class Meta:
        verbose_name_plural = 'Suppliers'
        ordering = ['name']


class Patient(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='gender')
    address = models.CharField(max_length=100, blank=True, verbose_name='address')
    phone = models.CharField(max_length=30, blank=True, verbose_name='phone')
    dob = models.CharField(max_length=30, verbose_name='Date of Birth', help_text='Please enter date of birth in format:dd/mm/yy', blank=True)
    age = models.PositiveSmallIntegerField(default=0,verbose_name='age')

    class Meta:
        verbose_name_plural = 'Patients'
        ordering = ['first_name']

    def __unicode__(self):

        return u'%s %s' % (self.first_name, self.last_name)

    def _get_full_name(self):
        """returns the person's full name"""

        return '%s  %s' % (self.first_name, self.last_name)

    full_name = property(_get_full_name)


class Staff(models.Model):
    first_name = models.CharField(max_length=30,verbose_name='First Name')
    last_name = models.CharField(max_length=30,verbose_name='Last Name')
    phone = models.CharField(max_length=30,verbose_name='phone')
    alternate_phone = models.CharField(max_length=30,blank=True,verbose_name='Alternate Phone')
    email = models.EmailField(blank=True,verbose_name='email')
    designation = models.CharField(max_length=50,choices=STAFF_DESIGNATION,verbose_name='designation')

    class Meta:
        verbose_name_plural = 'Staff'
        ordering =['first_name']

    def __unicode__(self):

        return u'%s %s' % (self.first_name, self.last_name)

    def _get_full_name(self):
        """ returns the person's full name """

        return u'%s  %s' % (self.first_name, self.last_name)

    full_name = property(_get_full_name)


class LabTest(models.Model):
    type = models.CharField(max_length=100, verbose_name="name")
    unit_cost = models.PositiveIntegerField(default=0, verbose_name='Unit Cost')

    def __unicode__(self):
        return u'%s' % self.type

    class Meta:
        verbose_name_plural = 'Lab Tests'
        ordering = ['type']


class Item(models.Model):
    name = models.CharField(max_length=100,verbose_name="Drug Name")
    quantity = models.PositiveIntegerField(default=0,verbose_name="quantity")
    unit_cost = models.PositiveIntegerField(default=0,verbose_name="Retail Price")
    cost_price = models.PositiveIntegerField(default=0,verbose_name="Wholesale Price")

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name_plural = 'Prescription Drugs'
        ordering = ['name']


class Visit(models.Model):
    patient_id = models.ForeignKey(Patient, verbose_name="patient")
    category = models.CharField(max_length=10, choices=CLINIC_TYPE, verbose_name="Visit Type")
    diagnosis = models.TextField(verbose_name="diagnosis")
    attendant = models.ForeignKey(Staff, verbose_name='attendant')
    consultation = models.BooleanField(default='True', verbose_name="consultation")
    visit_date = models.DateTimeField(auto_now_add=True, verbose_name="Visit Date")
    lab_tests = models.ManyToManyField(LabTest, verbose_name=' Lab Tests', through='VisitTest')
    prescriptions = models.ManyToManyField(Item, verbose_name='Prescriptions',  through='VisitItem')

    class Meta:
        verbose_name_plural = 'Clinic Visits'

    def lab_test_names(self):
        '''return names of lab tests for each visit '''

        return ', '.join([a.type for a in self.lab_tests.all()])

    def prescription_names(self):
        """return prescriptions for a given visit"""

        return ','.join([a.name for a in self.prescriptions.all()])

    lab_test_names.short_description = 'Lab Tests'
    prescription_names.short_description = 'Prescriptions'


class VisitTest(models.Model):
    test = models.ForeignKey(LabTest)
    visit = models.ForeignKey(Visit)

    class Meta:

        verbose_name = 'lab test'
        verbose_name_plural = 'Lab Tests Taken'


class VisitItem(models.Model):
    item = models.ForeignKey(Item)
    visit = models.ForeignKey(Visit)
    quantity = models.PositiveIntegerField(default=0, verbose_name="quantity")

    class Meta:
        verbose_name = 'prescription'
        verbose_name_plural = 'Prescribed Drugs'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        super(VisitItem, self).save(False, False, None, None)

        #update quantity field in Parent Model item

        self.item.quantity -= self.quantity

        self.item.save()





