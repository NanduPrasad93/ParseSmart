from django import forms
from . models import Candidate, Company_vaccancy,Expert,Appoinment,Complaint,Tips,Study_materials, Notification, CentralGovJob
from .models import Appoinment,Resource,Resume,Company,Chat
from .models import SpecialRegistration



class Candidate_Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['Name', 'Gender', 'Contact', 'Email', 'Password']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Name'}),
            'Gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Gender'}),
            'Contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Contact'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}),
            'Password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'}),
        }
class LoginForm(forms.Form):
    Email = forms.EmailField(label="Email", max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}))
    Password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'}))  




class SpecialRegistrationForm(forms.ModelForm):
    Dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date of Birth"
    )

    class Meta:
        model = SpecialRegistration
        fields = [
            'Candidate_name', 'Fathers_name', 'Phone_no', 'Email_id',
            'Highest_qua', 'Dob', 'Gender', 'Caste', 'Height', 'Weight',
             'nationality', 'marital_status', 'languages_known', 'disability_status'
        ]
        widgets = {
            'Candidate_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Candidate Name'}),
            'Fathers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Father\'s Name'}),
            'Phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'Email_id': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email ID'}),
            'Highest_qua': forms.Select(attrs={'class': 'form-control'}, choices=SpecialRegistration.Highest_qua),
            'Gender': forms.Select(attrs={'class': 'form-control'}, choices=SpecialRegistration.Gender),
            'Caste': forms.Select(attrs={'class': 'form-control'}, choices=SpecialRegistration.Caste),
            'Height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Height (in cm)'}),
            'Weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Weight (in kg)'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}, choices=SpecialRegistration.NATIONALITY_CHOICES),
            'marital_status': forms.Select(attrs={'class': 'form-control'}, choices=SpecialRegistration.MARITAL_CHOICES),
            'languages_known': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., English, Hindi, Tamil'}),
            'disability_status': forms.Select(attrs={'class': 'form-control'}, choices=SpecialRegistration.DISABILITY_CHOICES),
        }

class Edit_Form(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES
    )

    class Meta:
        model = Candidate
        fields = ['Name', 'Gender', 'Contact', 'Email']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Name'}),
            'Gender': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px; height: 40px; border: none; border-bottom: 1px solid #333; background-color: transparent;'}),
            'Contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Contact'}),
            'Email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Enter your Email'}),
        }





# class SpecialRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = SpecialRegistration
#         fields = ['Candidate_name', 'Fathers_name', 'Phone_no','Email_id', 'Highest_qua', 'Tenth_percentage','Twelfth_percentage', 'UG_percentage', 'PG_percentage', 'Dob','Gender','Pincode','Caste','Religion','Address','Landmark','Height','Weight','Chest_size','Sports','Ncc','Photo']

    




class Expert_Form(forms.ModelForm):
    class Meta:
        model = Expert
        fields = ['Name', 'Contact', 'Email', 'Password', 'Field', 'Designation', 'Year_of_experience', 'LinkedIn', 'Achievements']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'Contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your number'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'Password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Enter your Password'}),
            'Field': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your field'}),
            'Designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job title or role'}),
            'Year_of_experience': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'Years'}),
            'LinkedIn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your link'}),
            'Achievements': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your achievements'}),
        }
 

class ExpertLoginForm(forms.Form):
    Email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))




class Appoinment_Form(forms.ModelForm):
    class Meta:
        model = Appoinment
        fields = ['Date', 'Time']
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
            'Time': forms.TimeInput(attrs={
                'type': 'time',
                'min': '06:00',      
                'max': '08:00',      
            }),
        }

class Complaint_Form(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['Complaint_Subject', 'complaint']
        widgets = {
            'Complaint_Subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complaint Subject'}),
            'complaint': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your complaint here'}),
        }

          
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your complaint here'})
        }


class Tips_Form(forms.ModelForm):
    class Meta:
        model = Tips
        fields = ['Tips']
        widgets = {
            'Tips': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Share Your Tips here'})
        }





class Material_Form(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('UPSC', 'UPSC'),
        ('SSC', 'SSC'),
        ('IBPS', 'IBPS'),
        ('CBSE', 'CBSE'),
        ('RBI', 'RBI'),
        ('RRB', 'RRB'),
        ('DEFENCE', 'DEFENCE')
    ]

    Category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'category-dropdown'}))
    
    Topic = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'topic-dropdown'}))

    File_upload = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control', 'id': 'file-upload'}))

    class Meta:
        model = Study_materials
        fields = ['Category', 'Topic', 'File_upload']

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)  # Get the selected category
        super().__init__(*args, **kwargs)

        # Dynamically set the Topic choices based on the category
        if category:
            topic_choices = {
                'UPSC': ['Indian Polity', 'History of India', 'Geography', 'Economy', 'Environment', 'Science and Technology', 'Current Affairs', 'World History', 'Indian Society', 'Internal Security', 'Disaster Management', 'Ethics, Integrity, and Aptitude','International Relations','Government Schemes and Policies','Environmental Issues','Science and Research','Social Issues','Agriculture','Infrastructure','Culture and Heritage','Public Administration','Defence and Security'],
                'SSC': ['History','Geography','Polity','Economy','Science and Technology','Environment', 'Current Affairs','Culture','Quantitative Aptitude','General Intelligence and Reasoning','English Language','General Science'],
                'IBPS': ['Reasoning Ability','Quantitative Aptitude','English Language','General Awareness','Computer Knowledge'],
                'CBSE': ['General Awareness','Quantitative Aptitude','Reasoning Ability','English Language','Computer Knowledge','Educational Psychology','Teaching Methodology','Subject-Specific Knowledge'],
                'RBI': ['Economic and Social Issues','Finance and Management','Quantitative Aptitude','Reasoning Ability','English Language','General Awareness','Computer Knowledge'],
                'RRB': ['General Awareness','Arithmetic','General Intelligence and Reasoning','General Science','Technical Subjects','Current Affairs','Computer Knowledge'],
                'DEFENCE': [ 'General Awareness','Current Affairs','Quantitative Aptitude','Reasoning Ability','English Language','General Science','History and Geography','National Security Issues','Military Technology','Defense Policies and Strategies']
            }

            # Set the Topic field's choices dynamically based on the selected category
            self.fields['Topic'].choices = [('', '-- Select Topic --')] + [(topic, topic) for topic in topic_choices.get(category, [])]
        else:
            # If no category is selected, keep Topic field empty
            self.fields['Topic'].choices = [('', '-- Select Topic --')]






class CentralGovJobForm(forms.ModelForm):
    class Meta:
        model = CentralGovJob
        fields = '__all__'  
        

class Notification_Form(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['Notifications']
        widgets = { 
            'Notifications': forms.Textarea(attrs={'cols': 80, 'rows': 20}), 
        }        

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'link', 'resource_type', 'field']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class Resume_Form(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']
        widgets = {
            'resume': forms.FileInput(attrs={'class': 'form-control'})
        }       

class Business_Form(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['Business_category', 'Business_name', 'Contact', 'Email', 'Password']

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['message']
        widgets = {
            'message': forms.Textarea()
        }

class CompanyLoginForm(forms.Form):
    Email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class Company_vaccancy_Form(forms.ModelForm):
    class Meta:
        model = Company_vaccancy
        fields = ['Job_category', 'Job_name', 'Job_description', 'Last_date_for_apply', 'Qualification']
        widgets = {
            'Job_description': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'class': 'form-control'}),
        }


