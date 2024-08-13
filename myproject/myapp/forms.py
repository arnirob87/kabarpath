from django import forms
from django.contrib.auth.forms import UserCreationForm
from ckeditor.widgets import CKEditorWidget
from .models import User, Application, Post, Comment, Product

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your email'
        })
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your phone number'
        })
    )
    referral_id = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customizing username field
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        # Customizing password1 field
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li>'
            '</ul>'
        )

        # Customizing password2 field
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''

        # Setting choices for referral_id field
        self.fields['referral_id'].widget.choices = self.get_referral_choices()

    def get_referral_choices(self):
        referred_users = User.objects.all().exclude(referral_id__isnull=True)
        choices = [(user.phone_number, user.username) for user in referred_users]
        choices.insert(0, ('', 'Select Referrer'))
        return choices

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'referral_id', 'profile_image', 'password1', 'password2')

class ProfileUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile Image', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'phone_number', 'email_address', 'address']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'thumbnail', 'image1', 'image2', 'image3', 'image4']
        widgets = {
            'content': CKEditorWidget(),  # Use CKEditorWidget for the content field
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['thumbnail', 'image1', 'image2', 'image3', 'image4']:
            self.fields[field_name].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'duration', 'start_date', 'end_date', 'price', 'product_pic1', 'product_pic2', 'product_pic3', 'product_pic4', 'thumb']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_pic1': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'product_pic2': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'product_pic3': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'product_pic4': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'thumb': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }