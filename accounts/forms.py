from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, UserPreference


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
            'class': 'w-full pl-10 pr-4 py-3 bg-surface-container-low border-transparent focus:border-primary focus:ring-1 focus:ring-primary rounded-xl text-body-md transition-all',
            'autocomplete': 'email',
        }),
        label='Email address',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full pl-10 pr-10 py-3 bg-surface-container-low border-transparent focus:border-primary focus:ring-1 focus:ring-primary rounded-xl text-body-md transition-all',
            'autocomplete': 'current-password',
        }),
        label='Password',
    )

    def clean_username(self):
        email = self.cleaned_data.get('username', '').lower().strip()
        return email


class SignUpForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'w-full pl-10 pr-4 py-3 bg-surface-container-low border-transparent focus:border-primary focus:ring-1 focus:ring-primary rounded-xl text-body-md transition-all',
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
            'class': 'w-full pl-10 pr-4 py-3 bg-surface-container-low border-transparent focus:border-primary focus:ring-1 focus:ring-primary rounded-xl text-body-md transition-all',
        }),
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full pl-10 pr-10 py-3 bg-surface-container-low border-transparent focus:border-primary focus:ring-1 focus:ring-primary rounded-xl text-body-md transition-all',
        }),
        help_text='Minimum 8 characters.',
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full pl-10 pr-10 py-3 bg-surface-container-low border-transparent focus:border-primary focus:ring-1 focus:ring-primary rounded-xl text-body-md transition-all',
        }),
    )
    agree_terms = forms.BooleanField(required=True, error_messages={'required': 'You must agree to the Terms & Privacy Policy.'})

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(username=email).exists():
            raise ValidationError("An account with this email already exists. Please sign in.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        email = self.cleaned_data['email'].lower()
        full_name = self.cleaned_data['full_name']
        password = self.cleaned_data['password']
        first_name, *last_parts = full_name.split()
        last_name = ' '.join(last_parts) if last_parts else ''
        user = User(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = UserProfile
        fields = ['avatar_url', 'bio', 'phone_number', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }


class PreferencesForm(forms.ModelForm):
    STYLE_CHOICES = [
        ('Adventure', 'Adventure'),
        ('Cultural', 'Cultural'),
        ('Beach', 'Beach'),
        ('Wildlife', 'Wildlife'),
        ('Wellness', 'Wellness'),
        ('Family', 'Family'),
        ('Solo', 'Solo'),
        ('Romantic', 'Romantic'),
        ('Foodie', 'Foodie'),
        ('Luxury', 'Luxury'),
    ]
    travel_styles = forms.MultipleChoiceField(
        choices=STYLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = UserPreference
        fields = [
            'budget_preference', 'travel_styles', 'pace_of_travel',
            'accommodation_preference', 'dietary_requirements',
            'email_notifications', 'sms_notifications', 'marketing_emails',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['travel_styles'] = self.instance.get_travel_styles()

    def save(self, commit=True):
        instance = super().save(commit=False)
        styles = self.cleaned_data.get('travel_styles', [])
        instance.set_travel_styles(list(styles))
        if commit:
            instance.save()
        return instance
