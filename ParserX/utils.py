
# from .models import Company_vaccancy, Vaccancy, Apply_vaccancy, Candidate, private_Apply_vaccancy

# def get_vacancy_applicants(vaccancy_id):
#     try:
#         # Fetch the specific vacancy
#         vacancy = Vaccancy.objects.get(id=vaccancy_id)

#         # Get all applications related to this vacancy
#         applications = Apply_vaccancy.objects.filter(vaccancy_id=vaccancy_id)

#         # Count of applicants
#         applicant_count = applications.count()

#         applicants = [
#             {"name": app.can_id.Name,"Gender": app.can_id.Gender,"email": app.can_id.Email,"contact":app.can_id.Contact}  # Adjust this based on Candidate fields
#             for app in applications
#         ]

#         # Return the data
#         return {
#             "vacancy": vacancy.Job_Title,
#             "applicant_count": applicant_count,
#             "applicants": applicants,
#         }

#     except Vaccancy.DoesNotExist:
#         # Handle case where the vacancy does not exist
#         return {
#             "error": "Vacancy not found",
#         }


