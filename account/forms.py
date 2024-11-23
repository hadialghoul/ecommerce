from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User 
from django import forms
from django.forms.widgets import PasswordInput,TextInput

class CreateUserForm(UserCreationForm):

    class Meta:
        model=User
        fields=('username','email','password1','password2')

    def __init__(self,*args,**kwargs):  # 3asehn n2dar nst3ml lfields constructor
        super(CreateUserForm,self).__init__(*args,**kwargs) #inheritance
        #3asehn n5ale lemail required
        self.fields['email'].required=True

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists(): ## eza mawjod bel database y3te error 
            raise forms.ValidationError('This is email is invalid')

        if len(email)>350: # eza length lal email aktr min 350 y3te error
            raise forms.ValidationError('Your email is to long')

        return email



class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=TextInput())
    password=forms.CharField(widget=PasswordInput())

#update form 
class UpdateUserForm(forms.ModelForm):
    password=None # badnash n3ml update lal password
    class Meta:
        model=User
        fields=['username','email']
        exclude=['password1','password2']

    def __init__(self,*args,**kwargs):  # 3asehn n2dar nst3ml lfields constructor
        super(UpdateUserForm,self).__init__(*args,**kwargs) #inheritance
        #3asehn n5ale lemail required
        self.fields['email'].required=True
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists(): ## eza mawjod bel database y3te error 
            raise forms.ValidationError('This is email is invalid')

        if len(email)>350: # eza length lal email aktr min 350 y3te error
            raise forms.ValidationError('Your email is to long')

        return email
   

   