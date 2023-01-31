from django import forms
from app.models import CandidateDetails,skills,qualifications,CustomUser



class candidateform(forms.ModelForm):

    choices=skills.objects.all()
    first_name=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your firstname'}))
    last_name=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your lastname'}))
    email=forms.EmailField(error_messages={'required':'*'},widget=forms.EmailInput(attrs={'class':'input','placeholder':'Enter your email '}))
    qualifications=forms.Select()  
    skills=forms.ModelMultipleChoiceField(error_messages={'required':'*'},queryset = skills.objects.all()) 
    experience=forms.IntegerField(error_messages={'required':'*'},widget=forms.NumberInput(attrs={'class':'input','placeholder':'Enter your experience'}))
    contact=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter mobile number'}))
    address=forms.CharField(error_messages={'required':'*'},widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your address'}))
    resume=forms.FileField()
    class Meta:
        model= CandidateDetails
        fields=['first_name','last_name','email','qualifications','skills','experience','contact','address','resume']
        error_messages = {
        
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
        model=CustomUser
        fields=['email','username','password','contact','role','accesslable']
        


   