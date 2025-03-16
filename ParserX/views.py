from datetime import timezone
import datetime
import json
from django.shortcuts import render,redirect,get_object_or_404

from ParserX.scraper import fetch_exam_dates
from .forms import Candidate_Form, ChatForm, Company_vaccancy_Form, CompanyLoginForm,LoginForm,Edit_Form, ReplyForm,Expert_Form,ExpertLoginForm,Appoinment_Form,Complaint_Form,Tips_Form,Material_Form, Notification_Form,ResourceForm,Resume_Form,Business_Form
from .models import MCQ, Appoinment, Candidate, Chat, Company, Company_vaccancy, Resource,Expert,Complaint,Tips,Study_materials,Notification,Resume, private_Apply_vaccancy, CentralGovJob
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password 
from django.db.models import Q 
from django.http import JsonResponse
from django.http import FileResponse, Http404
import os
from django.http import JsonResponse
from itertools import chain
from operator import attrgetter

from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Candidate
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


# from .utils import get_vacancy_applicants  # Import the function from utils.py
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse

import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tips


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import random
from django.shortcuts import render, redirect
from .models import Candidate, Tips


def Home(request):
    return render(request,'Home.html')
def admin1(request):
    return render(request,'admin.html')
def user_page(request):
    return render(request,'user_page.html')



def candidate(request):
    if request.method =='POST':
        form = Candidate_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    else:
        form = Candidate_Form()
    return render(request,'c_register.html',{'form':form})   
#Expert
def experts(request):
    if request.method == 'POST':
        form = Expert_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    else:
        form = Expert_Form()
    return render(request ,'Experts.html',{'form':form})
def accept(request,pk):
    user = get_object_or_404(Expert,id=pk)
    user.status = 1
    user.save()
    return redirect('expert_view')  
def reject(request,pk):
    user = get_object_or_404(Expert,id=pk)
    user.status = 2 
    user.save()
    return redirect('expert_view')  
#function for viewing the expert's details 
def expert_view(request):
    users = Expert.objects.all()
    candidate = Candidate.objects.all()
    com = Complaint.objects.all()
    company = Company.objects.all()
    return render(request, 'table-datatable.html',{'users':users,'var':candidate,'com':com, 'company':company})
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            password = form.cleaned_data['Password']
            try:
                user = Candidate.objects.get(Email=email)
                if user.Password == password:
                    request.session['user_id'] = user.id
                    return redirect('ppage')
                else:
                    messages.error(request, 'Invalid password')
            except Candidate.DoesNotExist:
                messages.error(request, 'User does not exist')
    else:
        form = LoginForm()
    return render(request,'login_index.html',{'form':form})  
def user_header(request):
    return render(request,'user_header.html')
def edit_profile(request):
    id=request.session['user_id']
    data = get_object_or_404(Candidate,id=id)
    if request.method == 'POST':
        var = Edit_Form(request.POST,instance=data)
        if var.is_valid():
            var.save()
            return redirect('edit_profile')
    else:
        var = Edit_Form(instance=data)
    return render(request,'c_profile.html',{'var':var})  
# def SpecialRegistration_view(request):
#     candidate_id = request.session.get('user_id')
#     can_id = Candidate.objects.get(id = candidate_id)
#     if request.method == 'POST':
#         form = SpecialRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             frm = form.save(commit=False)  # Save the form data to the database
#             frm.candidate_id = can_id
#             frm.save()
#             return redirect('user_page')  # Redirect to the success page after form submission
#     else:
#         form = SpecialRegistrationForm()
#     # Always return a response with the form, whether POST or GET
#     return render(request, 'SpecialRegForm.html', {'form': form})
def success_view(request):
    return render(request, 'success.html')
# def profile_view(request):
#     user_data =  request.session.get('user_id')
#     user_dta = Candidate.objects.get(id = user_data)
#     user_d = SpecialRegistration.objects.filter(candidate_id = user_dta)
#     return render(request,'Profile_s.html',{'var':user_d})
# def edit_special_profile(request):
#     user_id = request.session.get('user_id')  # Get the user from the session
#     profile = get_object_or_404(SpecialRegistration, candidate_id=user_id)
#     if request.method == 'POST':
#         form = SpecialRegistrationForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile_view')  # Redirect to profile view
#     else:
#         form = SpecialRegistrationForm(instance=profile)
#     return render(request, 'edit_special_profile.html', {'form': form})
# def delete_special_profile(request):
#     user_id = request.session.get('user_id')  # Get the user from the session
#     profile = get_object_or_404(SpecialRegistration, candidate_id=user_id)
#     if request.method == 'POST':
#         profile.delete()
#         return redirect('profile_view')  # Redirect to profile view
#     return render(request, 'confirm_delete.html', {'profile': profile})
def expert_login(request):
    if request.method == 'POST':
        form = ExpertLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            password = form.cleaned_data['password']
            try:
                # Fetch the expert user from the database
                expert = Expert.objects.get(Email=email)
                # Check if the related user exists and has a password
                if expert.Password:
                    # Check the expert's status
                    if expert.status == 1:  # Approved
                        # Verify the password using the related User object
                        if expert.Password == password:
                            request.session['expert_id'] = expert.id
                            return redirect('expert_home')
                        else:
                            return HttpResponse("Invalid password. Please try again.")
                    elif expert.status == 2:  # Rejected
                        return HttpResponse("Your account has been rejected by the admin. Contact support.")
                    else:
                        return HttpResponse("Your account is pending approval. Please wait for admin approval.")
                else:
                    return HttpResponse("The associated user account is not configured correctly.")
            except Expert.DoesNotExist:
                return HttpResponse("No account found with this email address.")
    else:
        form = ExpertLoginForm()
    return render(request, 'expert_login.html', {'form': form})
def admin_header(request):
    return render(request,'admin_header.html')
def expert_header(request):
    return render(request,'expert_header.html')
def expert_home(request):
    return render(request,'expert_home.html')
#for expert search
def search(request):
    user = request.GET.get('Designation')
    var = None
    if user:
        var = Expert.objects.filter(
            Q(Designation__icontains = user)
        )
    return render(request,'expert_search.html',{'user':user,'var':var})
def appointment(request,id):
    expert = get_object_or_404(Expert, id=id)
    candidate_id = request.session.get('user_id') 
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == 'POST':
        form = Appoinment_Form(request.POST)
        if form.is_valid():
            Date = form.cleaned_data['Date']
            Time = form.cleaned_data['Time']
            if Appoinment.objects.filter(Date=Date, Time=Time, e_id=expert).exists():
                messages.warning(request, 'The Slot is already taken')
            else:
                appointment = form.save(commit=False)
                appointment.e_id = expert
                appointment.c_id = candidate
                appointment.save()
                messages.success(request, 'Appointment created successfully!')
                return redirect('Home')  
    else:
        form = Appoinment_Form()
    return render(request, 'appoinment.html', {'form': form, 'expert': expert})
def appoint_view(request):
    id=request.session['expert_id']
    var = Appoinment.objects.filter(e_id=id)
    return render(request,'appoint_view.html',{'var':var})
def user_appoint(request):
    id=request.session['user_id']
    var = Appoinment.objects.filter(c_id=id)
    return render(request,'user_appoint.html',{'var':var})
def edit_appoinment(request,id):
    var = get_object_or_404(Appoinment,a_id = id)
    if request.method == 'POST':
        form = Appoinment_Form(request.POST,instance = var)
        if form.is_valid():
            form.save() 
            return redirect('user_appoint')
    else:
        form = Appoinment_Form(instance=var)
    return render(request,'edit_appoint.html',{'form':form})
def cad_cancel(request,id):
    var = get_object_or_404(Appoinment, a_id = id)
    var.status = 1
    var.save()
    return redirect('user_appoint')
def complaint(request):
    id = request.session['user_id']  # Get the user ID from the session
    user = get_object_or_404(Candidate, id=id)  # Get the Candidate object
    if request.method == 'POST':
        form = Complaint_Form(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.login_id = user  # Set the login_id field to the current user
            var.save()
            return redirect('user_page')  # Redirect to user page after saving
    else:
        form = Complaint_Form()
    return render(request, 'complaint.html', {'form': form})
def user_complaint(request):
    id=request.session['user_id']
    users = Candidate.objects.get(id=id)
    var = Complaint.objects.filter(login_id=users)
    return render(request,'user_complaint.html',{'var':var}) 
def delete_complaints(request,id):
    obj = get_object_or_404(Complaint,com_id=id)
    obj.delete()
    return redirect('user_complaint') 
def edit_complaints(request, id):
    user = get_object_or_404(Complaint, com_id=id)  # Fetch the complaint using com_id
    if request.method == 'POST':
        form = Complaint_Form(request.POST, instance=user)  # Use `instance` to populate form
        if form.is_valid():
            form.save()
            return redirect('user_complaint')  # Redirect to the user complaints page
    else:
        form = Complaint_Form(instance=user)  # Initialize form with existing data
    return render(request, 'edit_complaints.html', {'form': form})
def Response(request,id):
    var=get_object_or_404(Complaint,com_id=id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            user=form.cleaned_data['reply']
            var.reply=user
            var.view_status = 1
            var.save()
            return redirect('Response',id=id)
    else:
        form = ReplyForm()
    return render(request,'response.html',{'form':form}) 
def user_complaint(request):
    id = request.session['user_id']
    users = Candidate.objects.get(id=id)
    var = Complaint.objects.filter(login_id=users)
    return render(request, 'user_complaint.html', {'var': var})


################################-TIP-###############################################
def Tip(request):
    id = request.session['expert_id']  # Get the user ID from the session
    user = get_object_or_404(Expert, id=id)  # Get the Candidate object
    if request.method == 'POST':
        form = Tips_Form(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.ex_id = user  # Set the login_id field to the current user
            var.save()
            return redirect('Tip')  # Redirect to user page after saving
    else:
        form = Tips_Form()
    return render(request, 'tips.html', {'form': form})
def tip_view(request):
    users = Tips.objects.all().order_by('current_date')
    return render(request, 'tip_view.html',{'users':users})
def edit_tview(request,id):
    user = get_object_or_404(Tips,t_id=id)  # Fetch the complaint using com_id
    if request.method == 'POST':
        form = Tips_Form(request.POST, instance=user)  # Use `instance` to populate form
        if form.is_valid():
            form.save()
            return redirect('tip_view')  # Redirect to the user complaints page
    else:
        form = Tips_Form(instance=user)  # Initialize form with existing data
    return render(request, 'edit_tips.html', {'form': form})
def remove_tips(request,id):
    obj = get_object_or_404(Tips,t_id=id)
    obj.delete()
    return redirect('tip_view') 
def ct_view(request):
    var = Tips.objects.all().order_by('current_date')
    return render(request, 'ct_view.html', {'var': var})



# @login_required
# def candidate_dashboard(request):
#     # Get all tips and select a random one
#     tips = list(Tips.objects.all())
#     if tips:
#         request.session['random_tip'] = random.choice(tips).Tips 
    
#     return render(request, 'candidate_dashboard.html')

# @csrf_exempt
# def clear_tip(request):
#     if 'random_tip' in request.session:
#         del request.session['random_tip']
#     return JsonResponse({'status': 'success'})



################################-END-TIP-###############################################

def study_materials(request):
    if request.method == 'POST':
        category = request.POST.get('Category', None) 
        form = Material_Form(request.POST,request.FILES,category=category)
        if form.is_valid():
            form.save()
            return redirect('admin1')
    else:
        form = Material_Form()
    return render(request,'materials.html',{'form':form})   
# Define the predefined topics
TOPICS = {
    'UPSC': ['Indian Polity', 'History of India', 'Geography', 'Economy'],
    'SSC': ['General Intelligence', 'Quantitative Aptitude'],
    'IBPS': ['Reasoning', 'English', 'General Awareness'],
    'CBSE': ['Mathematics', 'Science', 'Social Studies'],
    'RBI': ['Finance', 'Economy'],
    'RRB': ['Mathematics', 'Reasoning'],
    'DEFENCE': ['Physics', 'Chemistry', 'Mathematics'],
}
def fetch_topics(request):
    # Get the selected category from the GET request
    category = request.GET.get('category')
    # Fetch the corresponding topics
    topics = TOPICS.get(category, [])
    # Return the topics as a JSON response
    return JsonResponse({'topics': topics})
def materials_view(request):
    material = Study_materials.objects.all().order_by('current_date')
    return render(request,'study_materials_view.html',{'material': material})
def edit_study_material(request, id):
    material = get_object_or_404(Study_materials, s_id=id)
    if request.method == 'POST':
        form = Material_Form(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()  
            return redirect('materials_view') 
    else:
        form = Material_Form(instance=material)
    return render(request, 'edit_study_material.html', {'form': form})
def delete_study_material(request, id):
    material = get_object_or_404(Study_materials, s_id=id)
    material.delete()  
    return redirect('materials_view')  
def study_materials_display(request):
    category = request.GET.get('category')
    topic = request.GET.get('topic')
    if category and topic:
        # Order by current_date in descending order (most recent first for LIFO)
        materials = Study_materials.objects.filter(Category=category, Topic=topic).order_by('-current_date')
    else:
        materials = []
    return render(request, 'study_materials_display.html', {'materials': materials})
# Download file view
def download_file(request, file_id):
    material = get_object_or_404(Study_materials, s_id=file_id)
    file_path = material.File_upload.path
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{material.File_upload.name}"'
        return response
    else:
        return HttpResponse("File not found.", status=404)
#video-conference
def video_conference(request, pk):
    var_a = get_object_or_404(Appoinment,pk = pk )
    return render(request,'video_conference.html',{'var':var_a})
@csrf_exempt  
def save_appointment_url(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        if url:
            appointment = get_object_or_404(Appoinment, pk=pk)
            appointment.videocon_url = url
            appointment.conferencing_status = 1
            appointment.save()
            return JsonResponse({'success': True, 'message': 'URL saved successfully'})
        return JsonResponse({'success': False, 'message': 'No URL provided'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)





########################################################################################
########################################################################################
########################################################################################

from django.shortcuts import render, redirect
from .forms import CentralGovJobForm

def add_central_gov_job(request):
    if request.method == 'POST':
        form = CentralGovJobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin1')  
    else:
        form = CentralGovJobForm()
    
    return render(request, 'add_central_gov_job.html', {'form': form})




def central_gov_jobs_view(request):
    jobs = CentralGovJob.objects.all() 
    return render(request, 'central_gov_jobs_view.html', {'jobs': jobs})



from django.shortcuts import render, redirect, get_object_or_404
from .models import CentralGovJob
from .forms import CentralGovJobForm

def edit_central_gov_job(request, id):
    job = get_object_or_404(CentralGovJob, id=id)
    if request.method == 'POST':
        form = CentralGovJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('central_gov_jobs_view')  # Redirect to job listing
    else:
        form = CentralGovJobForm(instance=job)

    return render(request, 'edit_central_gov_job.html', {'form': form})


def delete_central_gov_job(request, id):
    job = get_object_or_404(CentralGovJob, id=id)
    job.delete()
    return redirect('central_gov_jobs_view')  # Redirect to job listing



# def SpecialRegistration_view(request):
#     candidate_id = request.session.get('user_id')
#     can_id = Candidate.objects.get(id = candidate_id)
#     if request.method == 'POST':
#         form = SpecialRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             frm = form.save(commit=False)  # Save the form data to the database
#             frm.candidate_id = can_id
#             frm.save()
#             return redirect('user_page')  # Redirect to the success page after form submission
#     else:
#         form = SpecialRegistrationForm()
#     # Always return a response with the form, whether POST or GET
#     return render(request, 'SpecialRegForm.html', {'form': form})




# def edit_special_profile(request):
#     user_id = request.session.get('user_id')  # Get the user from the session
#     profile = get_object_or_404(SpecialRegistration, candidate_id=user_id)
#     if request.method == 'POST':
#         form = SpecialRegistrationForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile_view')  # Redirect to profile view
#     else:
#         form = SpecialRegistrationForm(instance=profile)
#     return render(request, 'edit_special_profile.html', {'form': form})
# def delete_special_profile(request):
#     user_id = request.session.get('user_id')  # Get the user from the session
#     profile = get_object_or_404(SpecialRegistration, candidate_id=user_id)
#     if request.method == 'POST':
#         profile.delete()
#         return redirect('profile_view')  # Redirect to profile view
#     return render(request, 'confirm_delete.html', {'profile': profile})


from django.shortcuts import render, redirect
from .models import SpecialRegistration, Candidate
from .forms import SpecialRegistrationForm

def SpecialRegistration_view(request):
    # Get the candidate_id from the session
    candidate_id = request.session.get('user_id')
    if not candidate_id:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    try:
        # Fetch the candidate object
        can_id = Candidate.objects.get(id=candidate_id)
    except Candidate.DoesNotExist:
        return render(request, 'error.html', {'message': 'Candidate not found'})
    
    # Check if the candidate has already registered
    if SpecialRegistration.objects.filter(candidate_id=can_id).exists():
        return redirect('Sprofile_view')  # Redirect to the profile view if already registered
    
    if request.method == 'POST':
        form = SpecialRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.candidate_id = can_id  # Associate the candidate with the registration
            frm.save()
            return redirect('user_page')  # Redirect to the user page after successful submission
    else:
        form = SpecialRegistrationForm()
    
    return render(request, 'SpecialRegForm.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import SpecialRegistration, Candidate
from .forms import SpecialRegistrationForm

# def Sprofile_view(request):
#     candidate_id = request.session.get('user_id')
#     candidate = get_object_or_404(Candidate, id=candidate_id)

#     if request.method == 'POST':
#         form = SpecialRegistrationForm(request.POST)
#         if form.is_valid():
#             special_reg = form.save(commit=False)
#             special_reg.candidate_id = candidate
#             special_reg.save()
#             return redirect('user_page')
#     else:
#         form = SpecialRegistrationForm()

#     return render(request, 'SpecialRegForm.html', {'form': form})

def Sprofile_view(request):
    user_data =  request.session.get('user_id')
    user_dta = Candidate.objects.get(id = user_data)
    user_d = SpecialRegistration.objects.filter(candidate_id = user_dta)
    return render(request,'Profile_s.html',{'var':user_d})

def edit_special_profile(request, id):
    special_profile = get_object_or_404(SpecialRegistration, id=id)

    if request.method == 'POST':
        form = SpecialRegistrationForm(request.POST, request.FILES, instance=special_profile)
        if form.is_valid():
            form.save()
            return redirect('Sprofile_view') 
    else:
        
        form = SpecialRegistrationForm(instance=special_profile)

    return render(request, 'edit_special_profile.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect

def delete_special_profile(request, id):
    special_profile = get_object_or_404(SpecialRegistration, id=id)

    if request.method == 'POST':
        special_profile.delete()
        return redirect('Sprofile_view')  

    return render(request, 'confirm_delete.html', {'record': special_profile})


from django.db.models import Q
from django.shortcuts import render
def recommend_jobs(request):
    candidate_id = request.session.get('user_id')
    print(candidate_id)

    try:
        candid = Candidate.objects.get(id=candidate_id)
        print(candid)
    except Candidate.DoesNotExist:
        return render(request, 'recommendations.html', {'error': 'Candidate not found'})

    candidate_registration = SpecialRegistration.objects.filter(candidate_id=candid).first()
    if not candidate_registration:
        return render(request, 'recommendations.html', {
            'error': 'You have not created a Special Registration profile. Please complete your registration to view job recommendations.'
        })

    print(candidate_registration)

    qualification = candidate_registration.Highest_qua
    caste = candidate_registration.Caste

    # Calculate BMI and determine physical fitness
    height_in_meters = candidate_registration.Height / 100  
    bmi = candidate_registration.Weight / (height_in_meters ** 2)


    if bmi < 18.5:
        fitness_category = "Underweight"
        requires_physical_fitness = False 
    elif 18.5 <= bmi < 24.9:
        fitness_category = "Normal weight"
        requires_physical_fitness = True  
    elif 25 <= bmi < 29.9:
        fitness_category = "Overweight"
        requires_physical_fitness = False  
    else:
        fitness_category = "Obese"
        requires_physical_fitness = False  

    print(f"Candidate's Qualification: {qualification}, Caste: {caste}, Fitness Category: {fitness_category}, Requires Physical Fitness: {requires_physical_fitness}")


    filters = Q(required_qualifications__icontains=qualification)

    if caste == 'SC' or caste == 'ST':
        filters &= Q(age_limit_sc_st__isnull=False)
    elif caste == 'OBC':
        filters &= Q(age_limit_obc__isnull=False)
    else:  
        filters &= Q(age_limit_general__isnull=False)

    if requires_physical_fitness:
        filters &= Q(requires_physical_fitness=True)

    # Fetch eligible jobs
    eligible_jobs = CentralGovJob.objects.filter(filters)

    if not eligible_jobs:
        print("No eligible jobs found.")

    return render(request, 'recommendations.html', {
        'candidate': candidate_registration,
        'jobs': eligible_jobs,
        'fitness_category': fitness_category,
        'requires_physical_fitness': requires_physical_fitness  
    })
# def recommend_jobs(request):
#     # Retrieve candidate_id from session
#     candidate_id = request.session.get('user_id')
#     print(candidate_id)
#     # Fetch the Candidate instance using the ID stored in the session
#     try:
#         candid = Candidate.objects.get(id=candidate_id)
#         print(candid)
#     except Candidate.DoesNotExist:
#         return render(request, 'recommendations.html', {'error': 'Candidate not found'})
#     # Fetch SpecialRegistration for the candidate
#     candidate_registration = SpecialRegistration.objects.filter(candidate_id=candid).first()  # Get the first match or None
#     if not candidate_registration:
#         return render(request, 'recommendations.html', {'error': 'You have not created a Special Registration profile. Please complete your registration to view job recommendations.'})
#     print(candidate_registration)
#     qualification = candidate_registration.Highest_qua  # Get candidate's qualification
#     print(f"Candidate's Qualification: {qualification}")
#     # Fetch jobs matching candidate's qualification from Vaccancy model
#     eligible_jobs = Vaccancy.objects.filter(Q(Qualification__icontains=qualification))
#     if not eligible_jobs:
#         print("No eligible jobs found.")
#     return render(request, 'recommendations.html', {'candidate': candidate_registration, 'jobs': eligible_jobs})



def can_vaccancy(request):
    user_id = request.session.get('user_id')
    applied_vacancies = []

    if user_id:
        applied_vacancies = Apply_vaccancy.objects.filter(can_id=user_id).values_list('vaccancy_id', flat=True)

    var = Vaccancy.objects.all().order_by('Date')
    return render(request, 'can_vaccancy.html', {'var': var, 'applied_vacancies': applied_vacancies})
 
def apply(request, id):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "You need to log in to apply for a job.")
        return redirect('login')  # Redirects to the login page

    # Fetching user and vacancy objects
    user = get_object_or_404(Candidate, id=user_id)
    vacancy = get_object_or_404(Vaccancy, id=id)

    # Check if the user has already applied
    if Apply_vaccancy.objects.filter(can_id=user.id, vaccancy_id=vacancy.id).exists():
        messages.warning(request, "You have already applied for this job.")
    else:
        Apply_vaccancy.objects.create(can_id=user, vaccancy_id=vacancy)
        messages.success(request, "You have successfully applied for this job.")

    # Redirect back to the previous page (or fallback to can_vaccancy)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'can_vaccancy'))
#for the count and list of applicants(jan 11)
def vacancy_applicants_view(request, vaccancy_id):
    data = get_vacancy_applicants(vaccancy_id)
    return JsonResponse(data)




########################################################################################
########################################################################################
########################################################################################

def candidate_jobs_view(request):
    candidate_id = request.session.get('user_id')  
    applied_jobs = Apply_vaccancy.objects.filter(can_id=candidate_id).select_related('vaccancy_id')
    return render(request, 'candidate_jobs.html', {'applied_jobs': applied_jobs})
def cancel_application(request, application_id):
  
    application = Apply_vaccancy.objects.get(id=application_id)

    application.status = 1
    application.save()
    return redirect('candidate_jobs_view')

def vacancy_applicants_view(request, vaccancy_id):
    data = get_vacancy_applicants(vaccancy_id)
    return render(request, 'vacancy_applicants.html', {'data': data}) 
def add_notification(request):
    if request.method == 'POST':
        form = Notification_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notification_list')
    else:
        form = Notification_Form()
    return render(request, 'add_notification.html', {'form': form})
def notification_list(request):
    var = Notification.objects.all().order_by('current_date')
    return render(request, 'notification_list.html', {'var': var})
def edit_notification(request,id):
    var = get_object_or_404(Notification,n_id=id)
    if request.method == 'POST':
        form = Notification_Form(request.POST,instance = var)
        if form.is_valid():
            form.save() 
            return redirect('notification_list')
    else:
        form = Notification_Form(instance=var)
    return render(request,'edit_notification.html',{'form':form})
def remove_notification(request,id):
    obj = get_object_or_404(Notification,n_id=id)
    obj.delete()
    return redirect('notification_list')
def notify_list(request):
    var = Notification.objects.all().order_by('current_date')
    return render(request, 'notify_list.html', {'var': var})
def add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resources')  # Redirect to the resources listing page
    else:
        form = ResourceForm()
    return render(request, 'add_resource.html', {'form': form})
def resources(request):
    # Fetch all resources from the database
    resources_list = Resource.objects.all().order_by('added_on')  # Optionally, you can order by added date or title
    return render(request, 'resources.html', {'resources': resources_list})
def edit_resource(request,id):
    # Get the resource by ID or return 404 if not found
    resource = get_object_or_404(Resource,id=id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resources')  # Redirect to resources list page after successful update
    else:
        form = ResourceForm(instance=resource)  # Pre-fill form with existing resource data
    return render(request, 'edit_resource.html', {'form': form, 'resource': resource})
def remove_resources(request,id):
    obj = get_object_or_404(Resource,id=id)
    obj.delete()
    return redirect('resources')
def resources_by_field(request,field_name):
    print(f"Field selected: {field_name}")  # Debugging line
    resources = Resource.objects.filter(field=field_name)
    return render(request, 'resources_list.html', {'field_name': field_name, 'resources': resources})
def select_field(request):
    # Display the list of fields to choose from
    fields = [
        ('UPSC', 'UPSC'),
        ('SSC', 'SSC'),
        ('IBPS', 'IBPS'),
        ('CBSE', 'CBSE'),
        ('RBI', 'RBI'),
        ('RRB', 'RRB'),
        ('DEFENCE', 'DEFENCE'),
        ('Others', 'Others')
    ]
    return render(request, 'select_field.html', {'fields': fields})
# def recommend_jobs(request):
#     # Retrieve candidate_id from session
#     candidate_id = request.session.get('user_id')
#     print(candidate_id)
#     # Fetch the Candidate instance using the ID stored in the session
#     try:
#         candid = Candidate.objects.get(id=candidate_id)
#         print(candid)
#     except Candidate.DoesNotExist:
#         return render(request, 'recommendations.html', {'error': 'Candidate not found'})
#     # Fetch SpecialRegistration for the candidate
#     candidate_registration = SpecialRegistration.objects.filter(candidate_id=candid).first()  # Get the first match or None
#     if not candidate_registration:
#         return render(request, 'recommendations.html', {'error': 'You have not created a Special Registration profile. Please complete your registration to view job recommendations.'})
#     print(candidate_registration)
#     qualification = candidate_registration.Highest_qua  # Get candidate's qualification
#     print(f"Candidate's Qualification: {qualification}")
#     # Fetch jobs matching candidate's qualification from Vaccancy model
#     eligible_jobs = Vaccancy.objects.filter(Q(Qualification__icontains=qualification))
#     if not eligible_jobs:
#         print("No eligible jobs found.")
#     return render(request, 'recommendations.html', {'candidate': candidate_registration, 'jobs': eligible_jobs})
# -----------------------------------------------------------------------------------------------------
def upload_resume(request):
    id=request.session['user_id']
    var=get_object_or_404(Candidate,id=id)
    if Resume.objects.filter(candidate=var).exists():
        return render(request,'test.html')
    if request.method == "POST":
        form = Resume_Form(request.POST, request.FILES)
        if form.is_valid():
            f=form.save(commit=False)
            f.candidate = var
            f.save()
            return redirect('users_page')  
    else:
        form = Resume_Form()
    return render(request, 'upload_resume.html', {'form': form})
# -------------------------------------------------------------------------------------------------
def company(request):
    if request.method =='POST':
        form = Business_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    else:
        form = Business_Form()
    return render(request,'com_register.html',{'form':form})  
def com_accept(request,pk):
    company = get_object_or_404(Company,id=pk)
    company.com_status = 1
    company.save()
    return redirect('expert_view')  
def com_reject(request,pk):
    company = get_object_or_404(Company,id=pk)
    company.com_status = 2 
    company.save()
    return redirect('expert_view')  
def com_login(request):
    if request.method == 'POST':
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            password = form.cleaned_data['password']
            try:
                company = Company.objects.get(Email=email)
                if company.com_status == 1:  # Approved
                    if company.Password == password:  # Checking plain text password
                        request.session['company_id'] = company.id
                        return redirect('company_page')
                    else:
                        return render(request, 'com_login.html', {'form': form, 'error': "Invalid password. Please try again."})
                elif company.com_status == 2:  # Rejected
                    return render(request, 'com_login.html', {'form': form, 'error': "Your account has been rejected by the admin."})
                else:
                    return render(request, 'com_login.html', {'form': form, 'error': "Your account is pending approval."})
            except Company.DoesNotExist:
                return render(request, 'com_login.html', {'form': form, 'error': "No account found with this email."})
    else:
        form = CompanyLoginForm()
    return render(request, 'com_login.html', {'form': form})
def company_page(request):
    return render(request,'company_page.html')
def company_profile(request):
    id = request.session.get('company_id')
    company = Company.objects.filter(id=id).first()  # Get single object
    return render(request, 'company_profile.html', {'company': company})

def edit_company(request,id):
    var = get_object_or_404(Company,id=id)
    if request.method == 'POST':
        form = Business_Form(request.POST,instance = var)
        if form.is_valid():
            form.save() 
            return redirect('company_profile')
    else:
        form = Business_Form(instance=var)
    return render(request,'edit_company.html',{'form':form})

def remove_company(request,id):
    obj = get_object_or_404(Company,id=id)
    obj.delete()
    return redirect('company')

def com_header(request):
    return render(request,'com_header.html')

def users_page(request):
    return render(request,'puser_page.html')



def ppage(request):
    if request.method == "POST":
        sector = request.POST.get("sector")
        if sector == "public":
            return redirect("user_page")
        elif sector == "private":
            return redirect("users_page")
    return render(request,"abcdef.html") 


# -------------------------------------------------------------------------------------
def com_vaccancy(request):
    id=request.session['company_id']
    var=get_object_or_404(Company,id=id)
    if request.method =='POST':
        form = Company_vaccancy_Form(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.company = var
            form.save()
            return redirect('company_page')
    else:
        form = Company_vaccancy_Form()
    return render(request,'com_vaccancy.html',{'form':form})

def announce_interview(request, id):
    if request.method == "POST":
        interview_datetime = request.POST.get('interview_datetime')
        vacancy = get_object_or_404(Company_vaccancy, id=id)
        vacancy.interview_datetime = parse_datetime(interview_datetime)
        vacancy.save()
        messages.success(request, "Interview date & time updated successfully!")
    
    return redirect('private_vaccancy_view')

def private_vaccancy_view(request):
    id = request.session.get('company_id')  # Use .get() to avoid KeyError

    if not id:  
        return render(request, 'private_vaccancy_view.html', {'var': []})  

    company = get_object_or_404(Company, id=id)  
    company_vacancies = Company_vaccancy.objects.filter(company=company).order_by('Last_date_for_apply')  

    if request.method == "POST":
        vacancy_id = request.POST.get("vacancy_id")
        interview_date = request.POST.get("interview_date")

        if vacancy_id and interview_date:
            vacancy = get_object_or_404(Company_vaccancy, id=vacancy_id, company=company)
            vacancy.interview_date = interview_date
            vacancy.save()
    
    return render(request, 'private_vaccancy_view.html', {'var': company_vacancies})
 


def edit_com_vaccancy(request,id):
    var = get_object_or_404(Company_vaccancy,id=id)
    if request.method == 'POST':
        form = Company_vaccancy_Form(request.POST,instance = var)
        if form.is_valid():
            form.save() 
            return redirect('private_vaccancy_view')
    else:
        form = Company_vaccancy_Form(instance=var)
    return render(request,'private_edit_vaccancy.html',{'form':form})

def remove_com_vaccancy(request,id):
    obj = get_object_or_404(Company_vaccancy,id=id)
    obj.delete()
    return redirect('private_vaccancy_view')

def private_can_vaccancy(request):
    var = Company_vaccancy.objects.all().order_by('Last_date_for_apply')
    return render(request, 'private_can_vaccancy.html', {'var': var})  

def private_apply(request, id):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to apply for a job.")
        return redirect('login')  

    user = get_object_or_404(Candidate, id=user_id)
    pvacancy = get_object_or_404(Company_vaccancy, id=id)

    if private_Apply_vaccancy.objects.filter(private_can_id=user, private_vaccancy_id=pvacancy).exists():
        messages.warning(request, "You have already applied for this job.")
    else:
        private_Apply_vaccancy.objects.create(private_can_id=user, private_vaccancy_id=pvacancy)
        messages.success(request, "You have successfully applied for this job.")

    return redirect('vacancy_detail', id=id)

def vacancy_detail(request, id):
    user_id = request.session.get('user_id')
    vacancy = get_object_or_404(Company_vaccancy, id=id)
    applied = False

    if user_id:
        user = get_object_or_404(Candidate, id=user_id)
        applied = private_Apply_vaccancy.objects.filter(private_can_id=user, private_vaccancy_id=vacancy).exists()

    return render(request, 'vacancy_detail.html', {'var': vacancy, 'applied': applied})
                   

def view_applicants(request, id):
    vacancy = get_object_or_404(Company_vaccancy, id=id)
    
    # Fetch all applications (active & cancelled)
    applications = private_Apply_vaccancy.objects.filter(
        private_vaccancy_id=vacancy
    ).select_related('private_can_id')

    applicants = []
    for app in applications:
        candidate = app.private_can_id
        resume = Resume.objects.filter(candidate=candidate).first()  
        applicants.append({
            'id': app.pk,
            'candidate': candidate, 
            'resume': resume, 
            'applied_on': app.current_date, 
            'status': "Cancelled" if app.p_status == 1 else "Active"
        })

    return render(request, 'view_applicants.html', {'vacancy': vacancy, 'applicants': applicants})


from datetime import datetime

def view_applied_jobs(request):
    candidate_id = request.session.get('user_id')  

    if not candidate_id:
        return render(request, 'applied_jobs.html', {'var': []})  

    candidate = get_object_or_404(Candidate, id=candidate_id)
    applied_jobs = private_Apply_vaccancy.objects.filter(private_can_id=candidate).select_related('private_vaccancy_id')

   
    job_details = []
    for app in applied_jobs:
        job = app.private_vaccancy_id
        job_details.append({
            'job_name': job.Job_name,
            'job_category': job.Job_category,
            'job_description': job.Job_description,
            'applied_on': app.current_date,
            'interview_datetime': job.interview_datetime,
            'interview_url': job.videocon_url
        })

    return render(request, 'applied_jobs.html', {'var': job_details})


# def view_applied_jobs(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         messages.error(request, "You need to log in to view applied jobs.")
#         return redirect('login')  

#     candidate = get_object_or_404(Candidate, id=user_id)
#     applied_jobs = private_Apply_vaccancy.objects.filter(private_can_id=candidate).select_related('private_vaccancy_id')

#     jobs = []
#     for application in applied_jobs:
#         jobs.append({
#             'id': application.id,  # Include application ID for canceling
#             'job': application.private_vaccancy_id,
#             'applied_on': application.current_date,
#             'status': application.p_status  # Use `p_status` to track cancellation
#         })

#     return render(request, 'applied_jobs.html', {'jobs': jobs})

def private_cancel_application(request, application_id):
    application = get_object_or_404(private_Apply_vaccancy, id=application_id)
    application.p_status = 1  # Mark as cancelled
    application.save()
    return redirect('view_applied_jobs')



# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
#                           'CHAT'
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Candidate, Expert
from .forms import ChatForm

def chat_exp(request, pk):
    candidate = get_object_or_404(Candidate, id=request.session.get('user_id'))
    expert = get_object_or_404(Expert, id=pk)
    
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.candidate_sender = candidate
            chat.expert_receiver = expert
            chat.save()
            return redirect('chat_exp', pk=pk)
    else:
        form = ChatForm()
    
    messages = Chat.objects.filter(candidate_sender=candidate, expert_receiver=expert)
    messages = messages.union(Chat.objects.filter(expert_sender=expert, candidate_receiver=candidate)).order_by('current_time')
    
    return render(request, 'chat.html', {
        'msgs': messages,
        'candidate_sender': candidate,
        'expert_receiver': expert,
        'form': form
    })

def chat_temp(request, pk):
    expert = get_object_or_404(Expert, id=request.session.get('expert_id'))
    candidate = get_object_or_404(Candidate, id=pk)
    
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.expert_sender = expert
            chat.candidate_receiver = candidate
            chat.save()
            return redirect('chat_temp', pk=pk)
    else:
        form = ChatForm()
    
    messages = Chat.objects.filter(expert_sender=expert, candidate_receiver=candidate)
    messages = messages.union(Chat.objects.filter(candidate_sender=candidate, expert_receiver=expert)).order_by('current_time')
    
    return render(request, 'chat.html', {
        'msgs': messages,
        'expert_sender': expert,
        'candidate_receiver': candidate,
        'form': form
    })

# def chats_list(request):
#     expert = get_object_or_404(Expert, id=request.session.get('expert_id'))
#     candidates = Candidate.objects.filter(candidatesent_messages__expert_receiver=expert).distinct()
    
#     return render(request, 'chatlist_exp.html', {'candidates': candidates})

def chats_list(request):
    id = request.session.get('expert_id')
    expert = get_object_or_404(Expert, pk=id)  

    # Get distinct candidates the expert has chatted with
    var = Chat.objects.filter(expert_sender=expert).values_list('candidate_receiver__Name', 'candidate_receiver_id', flat=False).distinct()
    
    return render(request, 'chatlist_exp.html', {'var': var})

# def chats_list(request):
#     id = request.session.get('expert_id')
    
#     # Ensure the expert exists
#     expert = get_object_or_404(Expert, pk=id)  

#     # Get distinct candidates the expert has chatted with
#     var = Chat.objects.filter(expert_sender=expert).values_list(
#         'candidate_receiver__Name', 'candidate_receiver_id'
#     ).distinct()

#     return render(request, 'chatlist_exp.html', {'var': var})




# def chat_list(request):
#     candidate = get_object_or_404(Candidate, id=request.session.get('user_id'))
    
#     experts = Expert.objects.filter(
#         id__in=Chat.objects.filter(candidate_sender=candidate).values_list('expert_receiver', flat=True)
#     ).union(
#         Expert.objects.filter(
#             id__in=Chat.objects.filter(candidate_receiver=candidate).values_list('expert_sender', flat=True)
#         )
#     )

#     return render(request, 'chatlist_can.html', {'experts': experts})
# def chat_list(request):
#     candidate = get_object_or_404(Candidate, id=request.session.get('user_id'))
    
#     chats = Chat.objects.filter(
#         candidate_sender=candidate
#     ).values_list('expert_receiver__Name', 'expert_receiver__id').union(
#         Chat.objects.filter(
#             candidate_receiver=candidate
#         ).values_list('expert_sender__Name', 'expert_sender__id')
#     )

#     return render(request, 'chatlist_can.html', {'var': chats})
def chat_list(request):
    id = request.session['user_id']
    can = get_object_or_404(Candidate,pk = id)
    var = Appoinment.objects.filter(c_id=can).values_list('e_id__Name','e_id',flat=False).distinct()
    return render(request,'chatlist_can.html',{'var':var})

# ----------------------------------------------------------------------------------------------------




#video conference company

#video-conference


def video_conference_company(request, pk):
    var_a = get_object_or_404(Company_vaccancy, pk=pk)
    return render(request, 'video_conference_company.html', {'var': var_a})


@csrf_exempt  
def interview_url(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')

            if not url:
                return JsonResponse({'success': False, 'message': 'No URL provided'}, status=400)

            job = get_object_or_404(Company_vaccancy, pk=pk)
            job.videocon_url = url  
            job.conferencing_status = 1  
            job.save()

            return JsonResponse({'success': True, 'message': 'URL saved successfully', 'url': job.videocon_url})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


from django.shortcuts import render
from .scraper import fetch_defence_exam_dates, fetch_exam_dates  # Import scraper function
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def fetch_exam_dates(request):
    url = "https://www.freejobalert.com/upcoming-exam-dates-of-various-jobs/1835/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    exam_data = []
    table_rows = soup.find_all("tr")

    for row in table_rows[1:]:  # Skipping the header row
        cols = row.find_all("td")
        if len(cols) >= 3:
            exam_data.append({
                "release_date": cols[0].text.strip(),
                "exam_name": cols[1].text.strip(),
                "exam_date": cols[2].text.strip()
            })

    # Get search query
    query = request.GET.get("q")
    if query:
        exam_data = [exam for exam in exam_data if query.lower() in exam["exam_name"].lower()]

    return render(request, "latest_exams.html", {"exam_data": exam_data})






def defence_exams(request):
    exams = fetch_defence_exam_dates()
    return render(request, "defence_exams.html", {"exams": exams})




##################-MCQ-#################################



# def mcq_view(request):
#     questions = MCQ.objects.order_by('?')[:10]  # Fetch 10 random questions
#     return render(request, "mcq.html", {"questions": questions})






def get_mcqs(request, category):
    mcqs = MCQ.objects.filter(category=category).values("question", "option_a", "option_b", "option_c", "option_d")
    return JsonResponse(list(mcqs), safe=False)

def mcq_test(request):
    return render(request, 'mcq_test.html')














import whisper
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

# Load Whisper model once (outside the view function)
model = whisper.load_model("small")

@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']

        # Save the uploaded file temporarily
        file_path = f"temp_{audio_file.name}"
        try:
            with open(file_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            # Transcribe the audio file
            result = model.transcribe(file_path)

            # Return the transcription result
            return JsonResponse({"transcription": result["text"]})

        except Exception as e:
            # Handle errors during transcription
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            # Remove temporary file
            if os.path.exists(file_path):
                os.remove(file_path)

    return JsonResponse({"error": "No audio file provided"}, status=400)
