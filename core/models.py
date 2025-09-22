from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db import models
from django.utils import timezone
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('traveler', 'Traveler'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100, blank=True)
    profile_completed = models.BooleanField(default=False)  # ✅ Add this here

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
class TravelerProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='traveler_photos/', blank=True, null=True)
    profile_completed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username


class TravelPost(models.Model):
    THEME = (
        ('adventure', 'Adventure'),
        ('family', 'Family'),
        ('solo', 'Solo'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    theme = models.CharField(max_length=50, choices=THEME)
    photo = models.ImageField(upload_to='travel_photos/')
    
    # ✅ Add these two fields
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.title


# TravelPlan Model
class TravelPlan(models.Model):
    CHOICES = (
        ('adventure', 'Adventure'),
        ('family', 'Family'),
        ('solo', 'Solo'),
    )

    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    theme = models.CharField(max_length=50, choices=CHOICES )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plans_created')
    suggested_for = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plans_suggested')
    created_at = models.DateTimeField(default=timezone.now)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.created_by.username}'s plan to {self.destination}"

# Location Model
class Location(models.Model):
    THEME_CHOICES = (
        ('adventure', 'Adventure'),
        ('family', 'Family'),
        ('solo', 'Solo'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES)
    coordinates = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name


# PostReport Model
# PostReport Model
class PostReport(models.Model):
    post = models.ForeignKey(TravelPost, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Report on {self.post.title} by {self.reported_by.username}"

# ✅ Move this outside
class UserManagement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    

class TravelerManagement(models.Model):
    traveler = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Admin status for {self.traveler.username}"

class CurrentLocation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    update_note = models.TextField(blank=True)

# class Feedback(models.Model):
#     TYPE_CHOICES = (
#         ('feedback', 'Feedback'),
#         ('complaint', 'Complaint'),
#     )

#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES)
#     message = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, default='Open')  # Open, Resolved, Ignored

#     def __str__(self):
#         return f"{self.type.title()} from {self.user.username}"

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=[('Feedback', 'Feedback'), ('Complaint', 'Complaint')])
    status = models.CharField(max_length=20, default='Pending')  # Optional: for admin review
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}"
 

class Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports_made')
    post = models.ForeignKey(TravelPost, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')  # e.g. Pending, Reviewed, Rejected
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reported {self.post.title}"


class LocationUpdate(models.Model):
    location = models.CharField(max_length=100)
    update_note = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
