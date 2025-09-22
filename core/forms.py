from django import forms
from .models import CustomUser
from .models import UserProfile
from .models import TravelerProfile
from .models import TravelPost
from .models import TravelPlan
from .models import Location
from .models import PostReport
from .models import UserManagement
from .models import CurrentLocation
from .models import Feedback
from .models import LocationUpdate
from .models import TravelerManagement


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['name','username', 'email', 'password', 'role']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','profile_photo', 'phone_number', 'date_of_birth', 'gender']
class TravelerProfileForm(forms.ModelForm):
    class Meta:
        model = TravelerProfile
        fields = ['name', 'age', 'gender', 'photo']
 
class TravelPostForm(forms.ModelForm):
    class Meta:
        model = TravelPost
        fields = ['title', 'description', 'location', 'theme', 'photo', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

class TravelPlanForm(forms.ModelForm):
    class Meta:
        model = TravelPlan
        fields = ['destination','start_date','end_date','budget','theme']
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name','description','is_active','theme','coordinates']
class PostReportForm(forms.ModelForm):
    class Meta:
        model = PostReport
        fields = ['post','reason'] 
class ManageUserForm(forms.ModelForm):
    class Meta:
        model = UserManagement
        fields = ['is_verified', 'is_blocked', 'notes']

class TravelerAdminForm(forms.ModelForm):
    class Meta:
        model = TravelerManagement  # or Traveler
        fields = ['is_verified', 'is_blocked', 'notes']
class LocationUpdateForm(forms.ModelForm):
    class Meta:
        model = LocationUpdate
        fields = ['location', 'update_note', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['category', 'message']

 