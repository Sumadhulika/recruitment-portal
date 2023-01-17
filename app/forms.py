from django import forms
from app.models import CandidateDetails,appuser,skills,qualifications
from multiselectfield import MultiSelectField
# from rest_framework import fields, serializers

skill=skills.objects.values_list()
skill=tuple(skill)





class candidateform(forms.ModelForm):


    first_name=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your firstname'}))
    last_name=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your lastname'}))
    email=forms.EmailField(error_messages={'required':'*'},widget=forms.EmailInput(attrs={'class':'input','placeholder':'Enter your email '}))
    qualifications=forms.Select()  
    # skills=forms.ModelMultipleChoiceField(widget = forms.SelectMultiple,queryset = skills.objects.all() )
    # skills=forms.MultiSelectField(widget = forms.SelectMultiple,queryset = skills.objects.all() )
    # skills=MultiSelectField(choices=skill, max_choices=3, max_length=3)
    skills=forms.Select() 
    experience=forms.IntegerField(error_messages={'required':'*'},widget=forms.NumberInput(attrs={'class':'input','placeholder':'Enter your experience'}))
    contact=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter mobile number'}))
    address=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your address'}))

    class Meta:
        model= CandidateDetails
        fields=['first_name','last_name','email','qualifications','skills','experience','contact','address']
        error_messages = {
            'skills' : {
                'required' : '*'
            },
            'qualifications' : {
                'required' : '*'
            }

        }
class registration(forms.ModelForm):
    email=forms.EmailField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your email'}))
    username=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your name'}))
    password=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter password '}))
    contact=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter mobile number'}))
    role=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your role'}))
    accesslable=forms.IntegerField(error_messages={'required':'*'},widget=forms.NumberInput(attrs={'class':'input','placeholder':'Enter your accesslable'}))
    
    
    
    class Meta:
        model=appuser
        fields=['email','username','password','contact','role','accesslable']
        


   