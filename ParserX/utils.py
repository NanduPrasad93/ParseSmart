
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



# ParserX/utils.py
from textblob import TextBlob  

def analyze_response(answer):
    """AI-enhanced analysis with scoring."""
    blob = TextBlob(answer)
    sentiment_score = blob.sentiment.polarity  
    word_count = len(blob.words)

    important_keywords = ["leadership", "decision making", "ethics", "governance", "public service", "policy", "problem-solving"]
    matched_keywords = [word for word in important_keywords if word in answer.lower()]
    
    keyword_score = (len(matched_keywords) / len(important_keywords)) * 5 if important_keywords else 0  
    sentiment_points = (sentiment_score + 1) * 5  

    if word_count < 10:
        length_score = 2  
    elif word_count > 50:
        length_score = 4  
    else:
        length_score = 5  

    final_score = round(sentiment_points + length_score + keyword_score, 1)
    sentiment_feedback = "Your response is positive! Keep up the strong tone." if sentiment_score > 0.2 else "Your response is neutral, try adding enthusiasm."
    complexity_feedback = "Your response is well-structured!" if word_count > 10 else "Try providing more details."
    keyword_feedback = f"You included {len(matched_keywords)} important keywords. Keep using relevant terms!"

    feedback = f"{sentiment_feedback} {complexity_feedback} {keyword_feedback}"
    return feedback, min(final_score, 10)



