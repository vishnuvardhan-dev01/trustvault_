
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Document


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "category", "file"]

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")

        if uploaded_file:
            if uploaded_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(
                    "File size must not exceed 10 MB."
                )

        return uploaded_file

