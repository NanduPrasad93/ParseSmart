import json
from channels.generic.websocket import AsyncWebsocketConsumer
from textblob import TextBlob  
from .models import InterviewResponse, Candidate
from asgiref.sync import sync_to_async

class IASInterviewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to IAS Interview WebSocket!"}))

    async def disconnect(self, close_code):
        print("WebSocket Disconnected:", close_code)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format"}))
            return

        user_answer = data.get('answer', '')
        question = data.get('question', 'General Question')
        user_id = data.get('user_id', None)  

        feedback, score = self.analyze_response(user_answer)

        # Save response to database asynchronously
        if user_id:
            candidate = await self.get_candidate(user_id)
            if candidate:
                await self.save_to_db(candidate, question, user_answer, feedback, score)
            else:
                print("Candidate not found.")

        await self.send(text_data=json.dumps({"feedback": feedback, "score": score}))

    @sync_to_async
    def get_candidate(self, user_id):
        """Fetch Candidate object asynchronously."""
        try:
            return Candidate.objects.get(id=user_id)
        except Candidate.DoesNotExist:
            return None

    @sync_to_async
    def save_to_db(self, candidate, question, answer, feedback, score):
        """Save InterviewResponse asynchronously."""
        InterviewResponse.objects.create(
            candidate=candidate,
            question=question,
            answer=answer,
            score=score,
            feedback=feedback
        )
        print("Saved to DB!")

    def analyze_response(self, answer):
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
