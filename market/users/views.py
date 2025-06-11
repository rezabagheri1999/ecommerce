from pyexpat.errors import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.urls import reverse_lazy

from .models import UserProfile
from django.contrib.auth import login, get_user_model, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login ,logout ,authenticate
from .forms import BasicRegisterForm, ProfileCompletionForm, CustomLoginForm, ProfileEditForm, ContactForm, \
    CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth.decorators import login_required






def register(request):
    if request.method == 'POST':
        form = BasicRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Please complete your profile.")
            return redirect('/')
    else:
        form = BasicRegisterForm()
    return render(request, 'Register.html', {'form': form})


def complete_profile(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = ProfileCompletionForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.is_profile_complete = True
            request.user.save()
            messages.success(request, "Profile completed successfully!")
            return redirect('home')
    else:
        form = ProfileCompletionForm()
    return render(request, 'CompleteRegistering.html', {'form': form})


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return redirect('complete_profile')

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل شما با موفقیت به‌روزرسانی شد")
            return redirect('home')  # Or wherever you want to redirect
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'EditProfile.html', {'form': form})

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.


def logout_page(request):
    logout(request)
    return redirect('/')


def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # Replace with your home URL name

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")

                # Handle 'next' parameter
                next_url = request.POST.get('next', '')
                if next_url:
                    return redirect(next_url)
                return redirect('home')  # Replace with your home URL name
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = CustomLoginForm()

    # Get 'next' parameter from GET request
    next_url = request.GET.get('next', '')

    return render(request, 'Login.html', {
        'form': form,
        'next': next_url
    })


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            contact_message = form.save(commit=False)
            if request.user.is_authenticated:
                contact_message.user = request.user
            contact_message.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد. با تشکر از ارتباط شما!')
            return redirect('contact')
    else:
        form = ContactForm(user=request.user)

    return render(request, 'Contact.html', {
        'form': form,
        'user_authenticated': request.user.is_authenticated
    })




#
# 1. Password Reset View (Form to request reset)
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')

    # Optional: You can override form_valid for additional logic
    # def form_valid(self, form):
    #     # Add any pre-processing here
    #     return super().form_valid(form)

# 2. Password Reset Done View (Confirmation email sent)
class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password_reset_done.html'

    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additional_info'] = "Please check your spam folder if you don't see the email."
        return context

# 3. Password Reset Confirm View (Actual password change form)
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')

    # Optional: Add custom validation
    def form_valid(self, form):
        # Add any password validation logic here
        return super().form_valid(form)

# 4. Password Reset Complete View (Success page)
class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = reverse_lazy('login')
        return context

# 5. (Optional) Password Change View (for logged-in users)
class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('users:password_change_done')

# 6. (Optional) Password Change Done View
class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'password_change_done.html'