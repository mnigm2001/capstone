
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _

class Pill(models.Model):
    
    # Color Options
    COLOR_OPTIONS = [
        ('White', 'White'),
        ('Beige', 'Beige'),
        ('Black', 'Black'),
        ('Blue', 'Blue'),
        ('Brown', 'Brown'),
        ('Clear', 'Clear'),
        ('Gold', 'Gold'),
        ('Gray', 'Gray'),
        ('Green', 'Green'),
        ('Maroon', 'Maroon'),
        ('Orange', 'Orange'),
        ('Peach', 'Peach'),
        ('Pink', 'Pink'),
        ('Purple', 'Purple'),
        ('Red', 'Red'),
        ('Tan', 'Tan'),
        ('Yellow', 'Yellow'),
        ('Beige & Red', 'Beige & Red'),
        ('Black & Green', 'Black & Green'),
        ('Black & Teal', 'Black & Teal'),
        ('Black & Yellow', 'Black & Yellow'),
        ('Blue & Brown', 'Blue & Brown'),
        ('Blue & Gray', 'Blue & Gray'),
        ('Blue & Green', 'Blue & Green'),
        ('Blue & Orange', 'Blue & Orange'),
        ('Blue & Peach', 'Blue & Peach'),
        ('Blue & Pink', 'Blue & Pink'),
        ('Blue & White', 'Blue & White'),
        ('Blue & White Specks', 'Blue & White Specks'),
        ('Blue & Yellow', 'Blue & Yellow'),
        ('Brown & Clear', 'Brown & Clear'),
        ('Brown & Orange', 'Brown & Orange'),
        ('Brown & Peach', 'Brown & Peach'),
        ('Brown & Red', 'Brown & Red'),
        ('Brown & White', 'Brown & White'),
        ('Brown & Yellow', 'Brown & Yellow'),
        ('Clear & Green', 'Clear & Green'),
        ('Dark & Light Green', 'Dark & Light Green'),
        ('Gold & White', 'Gold & White'),
        ('Gray & Peach', 'Gray & Peach'),
        ('Gray & Pink', 'Gray & Pink'),
        ('Gray & Red', 'Gray & Red'),
        ('Gray & White', 'Gray & White'),
        ('Gray & Yellow', 'Gray & Yellow'),
        ('Green & Orange', 'Green & Orange'),
        ('Green & Peach', 'Green & Peach'),
        ('Green & Pink', 'Green & Pink'),
        ('Green & Purple', 'Green & Purple'),
        ('Green & Turquoise', 'Green & Turquoise'),
        ('Green & White', 'Green & White'),
        ('Green & Yellow', 'Green & Yellow'),
        ('Lavender & White', 'Lavender & White'),
        ('Maroon & Pink', 'Maroon & Pink'),
        ('Orange & Turquoise', 'Orange & Turquoise'),
        ('Orange & White', 'Orange & White'),
        ('Orange & Yellow', 'Orange & Yellow'),
        ('Peach & Purple', 'Peach & Purple'),
        ('Peach & Red', 'Peach & Red'),
        ('Peach & White', 'Peach & White'),
        ('Pink & Purple', 'Pink & Purple'),
        ('Pink & Red Specks', 'Pink & Red Specks'),
        ('Pink & Turquoise', 'Pink & Turquoise'),
        ('Pink & White', 'Pink & White'),
        ('Pink & Yellow', 'Pink & Yellow'),
        ('Red & Turquoise', 'Red & Turquoise'),
        ('Red & White', 'Red & White'),
        ('Red & Yellow', 'Red & Yellow'),
        ('Tan & White', 'Tan & White'),
        ('Turquoise & White', 'Turquoise & White'),
        ('Turquoise & Yellow', 'Turquoise & Yellow'),
        ('White & Blue Specks', 'White & Blue Specks'),
        ('White & Red Specks', 'White & Red Specks'),
        ('White & Yellow', 'White & Yellow'),
        ('Yellow & Gray', 'Yellow & Gray'),
        ('Yellow & White', 'Yellow & White'),
    ]
    ## Set specific options for shape: those options are:
    # Barrel, Capsule/Oblong, Character-shape, Egg-shape, Eight-sided, Oval, Figure eight-shape, Five-sided, Four-sided, Gear-shape, Heart-shape, Kidney-shape, Rectangle, Round, Seven-sided, Six-sided, Three-sided, U-shape
    SHAPE_OPTIONS = [
        ('Barrel', 'Barrel'),
        ('Capsule/Oblong', 'Capsule/Oblong'),
        ('Character-shape', 'Character-shape'),
        ('Egg-shape', 'Egg-shape'),
        ('Eight-sided', 'Eight-sided'),
        ('Oval', 'Oval'),
        ('Figure eight-shape', 'Figure eight-shape'),
        ('Five-sided', 'Five-sided'),
        ('Four-sided', 'Four-sided'),
        ('Gear-shape', 'Gear-shape'),
        ('Heart-shape', 'Heart-shape'),
        ('Kidney-shape', 'Kidney-shape'),
        ('Rectangle', 'Rectangle'),
        ('Round', 'Round'),
        ('Seven-sided', 'Seven-sided'),
        ('Six-sided', 'Six-sided'),
        ('Three-sided', 'Three-sided'),
        ('U-shape', 'U-shape'),
    ]
    name = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='images/')
    color = models.CharField(max_length=255, choices=COLOR_OPTIONS)
    strength = models.CharField(max_length=255)
    imprint = models.CharField(max_length=255)
    shape = models.CharField(max_length=255, choices=SHAPE_OPTIONS)

    # Optional fields
    generic_name = models.CharField(max_length=255, blank=True)
    size = models.SmallIntegerField(null=True, blank=True)
    symptoms = models.CharField(max_length=255, blank=True)
    side_effects = models.CharField(max_length=255, blank=True)
    prescription = models.BooleanField(default=False)

    # ## Aditional fields
    drug_class = models.CharField(max_length=255, blank=True)
    pregnancy = models.CharField(max_length=255, blank=True)
    CSA_schedule = models.CharField(max_length=255, blank=True)
    labeler_supplier = models.CharField(max_length=255, blank=True)
    national_drug_code = models.CharField(max_length=255, blank=True)
    inactive_ingredients = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class MedicalHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

class PillHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pill = models.ForeignKey(Pill, on_delete=models.CASCADE)
    date_taken = models.DateTimeField()
    dose = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

class PillScanHistory(models.Model):
    front_side = models.CharField(max_length=255)
    back_side = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    shape = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)
    results = models.ManyToManyField(Pill, related_name='search_history')

    def __str__(self):
        return f"{self.front_side} {self.back_side} {self.color} {self.shape} search on {self.searched_at}"

class UserScanHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pill_scan = models.ForeignKey(PillScanHistory, on_delete=models.CASCADE, related_name='user_scans')

    def __str__(self):
        return f"{self.user.username} scanned {self.pill_scan.front_side}"

class PillIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pill_intakes')
    pill = models.ForeignKey('Pill', on_delete=models.CASCADE, related_name='intakes')
    frequency_hours = models.IntegerField(null=True, help_text=_("Frequency of intake in hours. E.g., 24 for daily."))
    # intake_time = models.TimeField()
    quantity = models.IntegerField(null=True, default=1, help_text=_("Quantity of pills taken at each intake."))

    def __str__(self):
        frequency_in_days = self.frequency_hours / 24
        return f"{self.pill.name} - Every {frequency_in_days} day(s)"

class PillReminder(models.Model):
    pill_intake = models.ForeignKey(PillIntake, on_delete=models.CASCADE, related_name='reminders')
    reminder_time = models.TimeField(help_text=_("Time to remind user to take the pill."))
    active = models.BooleanField(default=True, help_text=_("Whether the reminder is active."))

    def __str__(self):
        return f"Reminder for {self.pill_intake.pill.name} at {self.reminder_time}"
