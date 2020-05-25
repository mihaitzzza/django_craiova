from django import forms
from users.models import MyUser, Profile
from django.contrib.auth import password_validation


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label='E-mail')
    password = forms.CharField(
        required=True,
        max_length=255,
        label='Password',
        widget=forms.PasswordInput,
    )


class RegisterForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=255, label='First Name')
    last_name = forms.CharField(required=True, max_length=255, label='Last Name')
    email = forms.EmailField(required=True, label='E-mail')
    password = forms.CharField(
        required=True,
        max_length=255,
        label='Password',
        widget=forms.PasswordInput,
    )
    password_confirm = forms.CharField(
        required=True,
        max_length=255,
        label='Confirm password',
        widget=forms.PasswordInput,
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        users = MyUser.objects.filter(email=email)

        if users.count() != 0:
            raise forms.ValidationError('E-mai already exists.')

        return email

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']

        if password_confirm != password:
            raise forms.ValidationError("Password confirm doesn't match")

        return password_confirm

    def save(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = MyUser.objects.create_user(email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()


class UploadFileForm(forms.Form):
    my_file = forms.FileField(required=True)


class UploadProfileImage(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class SetPassword(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
    )
    password_confirmation = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password, self.user)

        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password_confirmation != password:
            raise forms.ValidationError('Password confirmation mismatch.')

        return password_confirmation

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        self.user.set_password(password)

        if commit:
            self.user.save()

        return self.user
