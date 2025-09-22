from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from django.contrib import messages
from .utils import get_coordinates
import requests


from .models import (
    CustomUser, Report, UserProfile, TravelerProfile, TravelPost,
    TravelPlan, Location, PostReport, UserManagement,
    CurrentLocation, Feedback, TravelerManagement
)
from .forms import (
    RegistrationForm, UserProfileForm, TravelerProfileForm,
    TravelPostForm, TravelPlanForm, FeedbackForm,
    LocationUpdateForm, PostReportForm, ManageUserForm,TravelerAdminForm
)

  # ✅ Use this inside views, not at the top level

def my_index_view(request):
    return render(request, 'core/index.html')

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')  # Replace with your admin dashboard URL name
            else:
                return redirect('user_dashboard')  # Or traveler_dashboard
    return render(request, 'core/login.html')

@login_required
def dashboard(request):
    if request.user.groups.filter(name='Travelers').exists():
        return render(request, 'core/traveler_dashboard.html')

# User registration
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            # 🔐 Make sure this user is NOT an admin
            user.is_staff = False
            user.is_superuser = False

            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Role-based redirect
            if user.is_staff:
                return redirect('admin_dashboard')  # Replace with your actual admin dashboard URL name
            else:
                return redirect('user_dashboard')  # Or 'traveler_dashboard' if that's your user view
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def dashboard(request):
    if request.user.groups.filter(name='Travelers').exists():
        return render(request, 'core/traveler_dashboard.html')
    elif request.user.is_staff:
        return render(request, 'core/admin_dashboard.html')
    else:
        return render(request, 'core/user_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard_view(request):
    travelers = CustomUser.objects.filter(role='traveler')  # or your logic
    return render(request, 'core/admin_dashboard.html', {'travelers': travelers})


# @login_required
# def user_profile_view(request):
#     profile, created = UserProfile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             request.user.profile_completed = True  # ✅ Optional: mark profile as complete
#             request.user.save()
#             return redirect('user_dashboard')  # ✅ Redirect after saving
#     else:
#         form = UserProfileForm(instance=profile)

#     return render(request, 'core/user_profile.html', {'form': form})

@login_required
def user_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        # ─── DEBUG ───────────────────────────────────────────────
        print("Method:", request.method)
        print("Form valid:", form.is_valid())
        print("Form errors:", form.errors)
        # ────────────────────────────────────────────────────────

        if form.is_valid():
            form.save()
            request.user.profile_completed = True
            request.user.save()
            print("Redirecting to dashboard from user_profile_view")
            return redirect('user_dashboard')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'core/user_profile.html', {'form': form})




@login_required
def traveler_profile_view(request):
    profile, created = TravelerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = TravelerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('traveler_dashboard')  # ✅ Go to dashboard after saving
    else:
        form = TravelerProfileForm(instance=profile)

    return render(request, 'core/traveler_profile.html', {'form': form})


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = TravelPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user  # ✅ Correct field name
            post.save()
            return redirect('dashboard')  # ✅ Redirect to traveler dashboard
    else:
        form = TravelPostForm()
    return render(request, 'core/create_post.html', {'form': form})

def moderate_posts_view(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        new_status = request.POST.get('status')
        post = TravelPost.objects.get(id=post_id)
        post.status = new_status
        post.save()
        return redirect('moderate_posts')

    posts = TravelPost.objects.all()
    return render(request, 'core/moderate_posts.html', {'posts': posts})

@login_required
def create_plan_view(request):
    if request.method == 'POST':
        form = TravelPlanForm(request.POST)
        if form.is_valid():
            travel_plan = form.save(commit=False)
            travel_plan.user = request.user
            travel_plan.save()
            return redirect('my_plans')  # ✅ Redirect to plans list
    else:
        form = TravelPlanForm()

    return render(request, 'core/create_plan.html', {'form': form})

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.status = 'Open'
            feedback.save()
            messages.success(request, "Your feedback has been submitted.")  # ✅ Add here
            return redirect('dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'core/feedback.html', {'form': form})


@login_required
def update_location_view(request):
    if request.method == 'POST':
        form = LocationUpdateForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.user = request.user
            location.save()
            messages.success(request, "Location updated successfully.")  # ✅ Add here
            return redirect('dashboard')
    else:
        form = LocationUpdateForm()
    return render(request, 'core/update_location.html', {'form': form})


@login_required
def review_reports_view(request):
    try:
        reports = PostReport.objects.select_related('post', 'reported_by').order_by('-timestamp')
    except Exception as e:
        reports = []
        print("Error loading reports:", e)

    return render(request, 'core/review_reports.html', {
        'reports': reports
    })
@login_required
def my_posts_view(request):
    posts = TravelPost.objects.filter(user=request.user)
    return render(request, 'core/my_posts.html', {'posts': posts})
@login_required
def my_posts_view(request):
    user_posts = TravelPost.objects.filter(user=request.user)
    return render(request, 'core/my_posts.html', {'posts': user_posts})
@login_required
def my_reports_view(request):
    reports = Report.objects.filter(user=request.user).select_related('post').order_by('-timestamp')
    return render(request, 'core/my_reports.html', {'reports': reports})
@staff_member_required
def review_feedback_view(request):
    feedbacks = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'core/review_feedback.html', {'feedbacks': feedbacks})
@login_required
def my_feedback_view(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'core/my_feedback.html', {'feedbacks': feedbacks})
@login_required
def location_list_view(request):
    locations = Location.objects.all()
    return render(request, 'core/location_list.html', {'locations': locations})

@login_required
def user_dashboard_view(request):
    print("Entered user_dashboard_view")  # ✅ Confirm the view is triggered
    print("Profile completed:", request.user.profile_completed)  # ✅ Check the flag

    if not request.user.profile_completed:
        return redirect('complete_profile')  # Prevent access if profile is incomplete

    return render(request, 'core/user_dashboard.html')


@login_required
def traveler_dashboard_view(request):
    try:
        profile = TravelerProfile.objects.get(user=request.user)
        if not profile.name or not profile.age or not profile.gender:
            messages.warning(request, "Please complete your profile before accessing the dashboard.")
            return redirect('traveler_profile')  # 🚪 Send them to fill details
    except TravelerProfile.DoesNotExist:
        return redirect('traveler_profile')  # 🚪 No profile yet

    return render(request, 'core/traveler_dashboard.html')


@login_required
def explore_view(request):
    query = request.GET.get('q', '')
    posts = TravelPost.objects.all()

    if query:
        posts = posts.filter(location__icontains=query)

    return render(request, 'core/explore.html', {
        'posts': posts,
        'query': query
    })


@login_required
def all_posts_view(request):
    query = request.GET.get('q')

    try:
        posts = TravelPost.objects.select_related('user').order_by('-date')
        if query:
            posts = posts.filter(description__icontains=query)
    except Exception as e:
        posts = []
        print("Error loading posts:", e)

    return render(request, 'core/all_posts.html', {
        'posts': posts,
        'query': query,
    })

@login_required
def admin_edit_traveler_view(request, traveler_id):
    if not request.user.is_staff:
        return redirect('login')

    traveler = get_object_or_404(CustomUser, id=traveler_id)
    profile, created = TravelerProfile.objects.get_or_create(user=traveler)

    if request.method == 'POST':
        form = TravelerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Traveler profile updated.")
            return redirect('manage_travelers')  # Make sure this URL name exists
    else:
        form = TravelerProfileForm(instance=profile)

    return render(request, 'core/admin_dashboard.html', {'travelers': travelers})
@login_required
def report_post_view(request, post_id):
    post = get_object_or_404(TravelPost, id=post_id)

    if request.method == 'POST':
        reason = request.POST.get('reason')
        PostReport.objects.create(
            post=post,
            reported_by=request.user,
            reason=reason,
            status='Pending'
        )
        return redirect('traveler_dashboard')  # Or wherever you want to redirect

    return render(request, 'core/report_post.html', {'post': post})


@staff_member_required
def review_feedback_view(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')  # Sorted by newest
    return render(request, 'core/my_feedback.html', {'feedbacks': feedbacks})

@login_required
def complete_profile_view(request):
    from .models import TravelerProfile

    profile, created = TravelerProfile.objects.get_or_create(user=request.user)

    # Mark profile as complete without showing a form
    request.user.profile_completed = True
    request.user.save()

    return redirect('user_dashboard')

@login_required
def my_plans_view(request):
    plans = TravelPlan.objects.filter(user=request.user)
    return render(request, 'core/my_plans.html', {'plans': plans})

@login_required
def create_suggestion_view(request):
    users = User.objects.exclude(id=request.user.id)  # ✅ Now inside the view

    form = TravelPlanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        plan = form.save(commit=False)
        plan.created_by = request.user
        plan.suggested_for = User.objects.get(id=request.POST['suggested_for'])
        plan.save()
        return redirect('traveler_dashboard')

    return render(request, 'core/create_suggestion.html', {'form': form, 'users': users})

@login_required
def all_traveler_plans_view(request):
    plans = TravelPlan.objects.all().order_by('-start_date')  # newest first
    return render(request, 'core/all_traveler_plans.html', {'plans': plans})

# @login_required
# def user_suggestions_view(request):
#     # Show plans suggested specifically for this user
#     suggestions = TravelPlan.objects.filter(suggested_for=request.user)
#     return render(request, 'core/user_suggestions.html', {'suggestions': suggestions})
def get_coordinates(place_name):
    api_key = '1f2517a5482a4634af312aebb4c0e881'  # Replace with your actual key
    url = f'https://api.opencagedata.com/geocode/v1/json?q={place_name}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    if data['results']:
        loc = data['results'][0]['geometry']
        return loc['lat'], loc['lng']
    return None, None
@login_required
def create_location_view(request):
    if request.method == 'POST':
        form = LocationUpdateForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            lat, lng = get_coordinates(location.name)
            location.latitude = lat
            location.longitude = lng
            location.save()
            return redirect('location_list')
    else:
        form = LocationUpdateForm()
    return render(request, 'core/create_location.html', {'form': form})

def travel_plan_detail_view(request, plan_id):
    plan = get_object_or_404(TravelPlan, id=plan_id)
    return render(request, 'core/travel_plan_detail.html', {'plan': plan})
@login_required
def create_travel_plan_view(request):
    form = TravelPlanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        plan = form.save(commit=False)
        lat, lng = get_coordinates(plan.destination)
        plan.latitude = lat
        plan.longitude = lng
        plan.created_by = request.user
        plan.save()
        return redirect('traveler_dashboard')
    return render(request, 'core/create_travel_plan.html', {'form': form})
@login_required
def manage_user_view(request):
    user = request.user
    form = ManageUserForm(request.POST or None, instance=user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')  # or wherever you want to go

    return render(request, 'core/manage_user.html', {'form': form, 'user': user})
def index_view(request):
    return render(request, 'core/index.html')