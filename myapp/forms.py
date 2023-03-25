from django import forms
from .models import user_signup,mynotes,feedback

class signupForm(forms.ModelForm):
    class Meta:
        model=user_signup
        fields='__all__'
    

class notesForm(forms.ModelForm):
    class Meta:
        model=mynotes
        fields='__all__'
       
class updateForm(forms.ModelForm):
    class Meta:
        model=user_signup
        fields=['firstname','lastname','username','password','email','city','state','mobile']

class feedbackForm(forms.ModelForm):
    class Meta:
        model=feedback
        fields='__all__'


