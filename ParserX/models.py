from django.db import models
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.utils import timezone
import datetime
from django.contrib.auth.models import User





class Candidate(models.Model):
    Name = models.CharField(max_length=200)
    Gender = models.CharField(max_length=10, choices=[('M','Male'),('F','Female'),('O','Other')])
    Contact= models.CharField(max_length=12, validators=[RegexValidator(r'^\d{10,15}$', message="Enter a valid contact number.")])    
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=10)




class SpecialRegistration(models.Model):
    Gender = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    Caste = [
        ('SC', 'Scheduled Caste'),
        ('ST', 'Scheduled Tribe'),
        ('OBC', 'Other Backward Class'),
        ('UR', 'Unreserved'),
    ]

    Highest_qua = [
        ('10th','10th'),
        ('12th','12th'),
        ('UG','UG'),
        ('PG','PG'),
    ]
    NATIONALITY_CHOICES = [('IND', 'Indian'), ('OTH', 'Other')]
    MARITAL_CHOICES = [('S', 'Single'), ('M', 'Married'), ('W', 'Widowed'), ('D', 'Divorced')]
    DISABILITY_CHOICES = [('No', 'No Disability'), ('Yes', 'Person with Disability (PwD)')]


    Candidate_name = models.CharField(max_length=100)
    Fathers_name = models.CharField(max_length=100)
    Phone_no = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{10,15}$', message="Enter a valid contact number.")]) 
    Email_id = models.EmailField(unique=True)
    Highest_qua = models.CharField(max_length=20, choices=Highest_qua)
    Dob = models.DateField()
    Gender = models.CharField(max_length=1, choices=Gender)
    Caste = models.CharField(max_length=3, choices=Caste)
    Height = models.FloatField(help_text="Height in cm")
    Weight = models.FloatField(help_text="Weight in kg")
    candidate_id = models.ForeignKey("Candidate", on_delete=models.CASCADE, null=True)
    NATIONALITY_CHOICES = [('IND', 'Indian'), ('OTH', 'Other')]
    nationality = models.CharField(max_length=3, choices=NATIONALITY_CHOICES, default='IND')
    marital_status = models.CharField(max_length=1, choices=MARITAL_CHOICES, default='S')
    languages_known = models.CharField(max_length=200, help_text="Enter languages known, separated by commas (e.g., English, Hindi, Tamil)",default="English")
    disability_status = models.CharField(max_length=3, choices=DISABILITY_CHOICES, default='No')


    def get_age(self):
        today = date.today()
        return today.year - self.Dob.year - ((today.month, today.day) < (self.Dob.month, self.Dob.day))

    def recommend_jobs(self):
        age = self.get_age()

        jobs = CentralGovJob.objects.all()

        # Filter by caste-based age limit
        if self.Caste == 'OBC':
            jobs = jobs.filter(age_limit_obc__gte=age)
        elif self.Caste in ['SC', 'ST']:
            jobs = jobs.filter(age_limit_sc_st__gte=age)
        else:
            jobs = jobs.filter(age_limit_general__gte=age)

        # Filter by required qualifications
        qualification_order = {'10th': 1, '12th': 2, 'UG': 3, 'PG': 4}
        jobs = [job for job in jobs if qualification_order[job.required_qualifications] <= qualification_order[self.Highest_qua]]


        return jobs



    #expert data
class Expert(models.Model):
    Name = models.CharField(max_length=200)
    Contact = models.IntegerField(max_length=12, validators=[RegexValidator(r'^\d{10,15}$', message="Enter a valid contact number.")]) 
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=10)
    Field = models.CharField(max_length=10)
    Designation = models.CharField(max_length=100)
    Year_of_experience = models.IntegerField()
    status = models.IntegerField(default=0)
    Profile_Picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    LinkedIn = models.URLField(max_length=200, null=True, blank=True)
    Achievements = models.TextField(null=True, blank=True)


class Appoinment(models.Model):
    a_id = models.AutoField(primary_key=True)
    Date = models.DateField(null=True)
    Time = models.TimeField(null=True)
    def get_current_date():
        return datetime.date.fromisoformat(timezone.now().date().isoformat())

    current_date = models.DateField(null= True,default=get_current_date)
    c_id = models.ForeignKey(Candidate,on_delete=models.CASCADE,null=True)
    e_id = models.ForeignKey(Expert,on_delete=models.CASCADE,null=True)
    status = models.IntegerField(default=0)
    conferencing_status = models.IntegerField(default=0)
    videocon_url = models.CharField(max_length=100)

class Complaint(models.Model):
    com_id = models.AutoField(primary_key=True)
    Complaint_Subject = models.CharField( max_length=1000)
    complaint = models.CharField(max_length=1000)
    login_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, default=1)
    created_datetime = models.DateTimeField(default=datetime.datetime.now)
    view_status = models.IntegerField(default=0)
    reply = models.CharField(max_length=1000)

   
class Tips(models.Model):
    t_id = models.AutoField(primary_key=True)
    current_date = models.DateField(auto_now_add=True)
    Tips = models.CharField(max_length=5000)
    ex_id = models.ForeignKey(Expert,on_delete=models.CASCADE, null = True)

class Study_materials(models.Model):
    s_id = models.AutoField(primary_key=True)   
    Category = models.CharField(max_length=1000)
    Topic = models.CharField(max_length=1000)
    current_date = models.DateField(auto_now_add=True) 
    File_upload = models.FileField(upload_to='upload')
    





########################################################################################
########################################################################################
########################################################################################






class CentralGovJob(models.Model):
    job_title = models.CharField(max_length=255, unique=True)  # Job title (e.g., SSC CGL Officer, IBPS PO)
    department = models.CharField(max_length=255)  # Government department (e.g., Railways, Defence, Banking)
    field = models.CharField(max_length=255)  # Job category (e.g., SSC, UPSC, Banking)
    description = models.TextField()  # Brief job details
    required_qualifications = models.TextField()  # Eligibility criteria
    age_limit_general = models.CharField(max_length=50, blank=True, null=True)  # Age limit for General category
    age_limit_obc = models.CharField(max_length=50, blank=True, null=True)  # Age limit for OBC
    age_limit_sc_st = models.CharField(max_length=50, blank=True, null=True)  # Age limit for SC/ST
    selection_process = models.TextField(blank=True, null=True)  # Written exam, interview, etc.
    salary_range = models.CharField(max_length=100, blank=True, null=True)  # Pay scale or salary details
    vacancies = models.IntegerField(blank=True, null=True)  # Number of vacancies
    exam_frequency = models.CharField(max_length=100, blank=True, null=True)  # Annual, Bi-annual, etc.
    work_type = models.CharField(max_length=50, choices=[('Permanent', 'Permanent'), ('Contract', 'Contract')], blank=True, null=True)  # Permanent/Contract
    application_mode = models.CharField(max_length=50, choices=[('Online', 'Online'), ('Offline', 'Offline')], blank=True, null=True)  # Online/Offline
    requires_physical_fitness = models.BooleanField(default=False)  # True if physical fitness is required
    success_rate = models.FloatField(blank=True, null=True)  # Percentage of candidates who get selected
    site = models.URLField(blank=True, null=True)  # Official website for more details




  







########################################################################################
########################################################################################
########################################################################################

class Notification(models.Model):
    n_id = models.AutoField(primary_key=True)
    Notifications = models.CharField(max_length=2000)
    current_date = models.DateField(auto_now_add=True)

class Resource(models.Model):
    FIELD_CHOICES = [
        ('UPSC', 'UPSC'),
        ('SSC', 'SSC'),
        ('IBPS', 'IBPS'),
        ('CBSE', 'CBSE'),
        ('RBI','RBI'),
        ('RRB','RRB'),
        ('DEFENCE','DEFENCE'),
        ('Others', 'Others'),
    ]

    RESOURCE_TYPES = [
        ('YouTube', 'YouTube Channel'),
        ('Website', 'Website'),
        ('App', 'Mobile Application'),
        ('Others', 'Other Resources'),
    ]

    title = models.CharField(max_length=200)  # Title of the resource
    description = models.TextField(blank=True)  # A short description
    link = models.URLField()  # URL of the resource
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)  # Type of resource
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)  # Related field
    added_on = models.DateTimeField(auto_now_add=True)  # Timestamp for when the resource was added

    def __str__(self):
        return self.title
    
class Resume(models.Model):
    resume = models.FileField(upload_to='resumes/')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.resume.name 


class Company(models.Model):
    Business_category = models.CharField(max_length=200)
    Business_name = models.CharField(max_length=200)
    Contact = models.IntegerField(max_length=12, validators=[RegexValidator(r'^\d{10,15}$', message="Enter a valid contact number.")]) 
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=10)
    com_status = models.IntegerField(default=0)


class Chat(models.Model):
    message = models.TextField()  
    candidate_sender = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True, related_name="candidatesent_messages")
    candidate_receiver = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True, related_name="candidatereceived_messages")
    expert_sender = models.ForeignKey(Expert, on_delete=models.CASCADE, null=True, blank=True, related_name="expert_sent_messages")
    expert_receiver = models.ForeignKey(Expert, on_delete=models.CASCADE, null=True, blank=True, related_name="expert_received_messages")
    current_time = models.DateTimeField(auto_now_add=True)

class Company_vaccancy(models.Model):
    Job_category = models.CharField(max_length=100)
    Job_name = models.CharField(max_length=100)
    Job_description = models.CharField(max_length=500)
    Last_date_for_apply = models.DateField(null=True)
    Qualification = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    status = models.IntegerField(default=0)
    interview_datetime = models.DateTimeField(null=True, blank=True)
    videocon_url = models.URLField(max_length=500, null=True, blank=True)
    conferencing_status = models.IntegerField(default=0) 


class private_Apply_vaccancy(models.Model):
    private_can_id = models.ForeignKey(Candidate,on_delete=models.CASCADE, null = True)
    private_vaccancy_id = models.ForeignKey(Company_vaccancy,on_delete=models.CASCADE, null=True)
    current_date = models.DateField(auto_now_add=True)
    p_status = models.IntegerField(default=0) 


class MCQ(models.Model):
    category = models.CharField(max_length=100)  
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category} - {self.question[:50]}"
    
    


class InterviewResponse(models.Model):
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,null=True)
    question = models.TextField()
    answer = models.TextField()
    score = models.FloatField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

