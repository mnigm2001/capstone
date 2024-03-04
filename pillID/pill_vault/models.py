from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User

# class CustomUserManager(BaseUserManager):
#     # Your custom user manager logic here...
#     pass

# class User(AbstractBaseUser, PermissionsMixin):

#     # username = models.CharField(max_length=255, unique=True)
#     # email = models.EmailField(unique=True)
#     ## Remove this later
#     username = models.CharField(max_length=255, default="-")
#     email = models.EmailField(default="-")

#     # You need to add related_name to groups and user_permissions like so:
#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name='groups',
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         related_name="custom_user_set",
#         related_query_name="user",
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name="custom_user_set",
#         related_query_name="user",
#     )

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     objects = CustomUserManager()

#     # Rest of your model...


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

    # generic_name = models.CharField(max_length=255)
    # size = models.SmallIntegerField()
    # symptoms = models.CharField(max_length=255)
    # side_effects = models.CharField(max_length=255)
    # prescription = models.BooleanField(default=True)

    # ## Aditional fields
    # drug_class = models.CharField(max_length=255)
    # pregnancy = models.CharField(max_length=255)
    # CSA_schedule = models.CharField(max_length=255)
    # labeler_supplier = models.CharField(max_length=255)
    # national_drug_code = models.CharField(max_length=255)
    # inactive_ingredients = models.CharField(max_length=255)

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

# class PillIntake(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     pill = models.ForeignKey(Pill, on_delete=models.CASCADE)
#     intake_time = models.TimeField()
#     days_of_week = models.CharField(max_length=14)  # '1234567' for daily
#     quantity = models.IntegerField(default=1)
#     active = models.BooleanField(default=True)

# class Reminder(models.Model):
#     pill_intake = models.ForeignKey(PillIntake, on_delete=models.CASCADE)
#     reminder_time = models.TimeField()
#     repeat = models.BooleanField(default=True)

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class PillIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pill_intakes')
    pill = models.ForeignKey('Pill', on_delete=models.CASCADE, related_name='intakes')
    frequency = models.CharField(max_length=255, help_text=_("Frequency of intake, e.g., 'daily', 'twice a day', etc."))
    intake_time = models.TimeField()
    quantity = models.IntegerField(default=1, help_text=_("Quantity of pills taken at each intake."))

    def __str__(self):
        return f"{self.pill.name} - {self.frequency}"

class PillReminder(models.Model):
    pill_intake = models.ForeignKey(PillIntake, on_delete=models.CASCADE, related_name='reminders')
    reminder_time = models.TimeField(help_text=_("Time to remind user to take the pill."))
    active = models.BooleanField(default=True, help_text=_("Whether the reminder is active."))

    def __str__(self):
        return f"Reminder for {self.pill_intake.pill.name} at {self.reminder_time}"


# class Request
# image
# user
# status
    
# class Images(models.Model):
#  Contains all the images for a specific pill taken thus far
