from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-input',
        })
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'role-radio'}),
        initial='learner',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-input',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
            'class': 'form-input',
        })


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-input',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-input',
        })
    )


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'duration', 'cost', 'youtube_url', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Course Title',
                'class': 'form-input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe what students will learn...',
                'class': 'form-input form-textarea',
                'rows': 4,
            }),
            'category': forms.Select(attrs={
                'class': 'form-input',
            }),
            'duration': forms.TextInput(attrs={
                'placeholder': 'e.g. 4 weeks, 10 hours',
                'class': 'form-input',
            }),
            'cost': forms.NumberInput(attrs={
                'placeholder': 'Time Coins required',
                'class': 'form-input',
                'min': 1,
            }),
            'youtube_url': forms.URLInput(attrs={
                'placeholder': 'https://www.youtube.com/watch?v=...',
                'class': 'form-input',
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Course notes, resource links, etc.',
                'class': 'form-input form-textarea',
                'rows': 4,
            }),
        }
