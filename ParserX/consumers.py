import json
from channels.generic.websocket import AsyncWebsocketConsumer
from textblob import TextBlob  

class IASInterviewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to IAS Interview WebSocket!"}))

    async def disconnect(self, close_code):
        print("WebSocket Disconnected:", close_code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_answer = data.get('answer', '')

        feedback = self.analyze_response(user_answer)  # Call AI function
        await self.send(text_data=json.dumps({"feedback": feedback}))

    def analyze_response(self, answer):
        """AI-enhanced analysis using NLP"""
        blob = TextBlob(answer)
        sentiment_score = blob.sentiment.polarity  # Sentiment (-1 to 1)
        word_count = len(blob.words)

        # Determine sentiment feedback
        if sentiment_score > 0.2:
            sentiment_feedback = "Your response has a positive tone. Keep it up!"
        elif sentiment_score < -0.2:
            sentiment_feedback = "Your response seems a bit negative. Try a more optimistic approach."
        else:
            sentiment_feedback = "Your response is neutral. Adding personal insights can make it more engaging."

        # Determine complexity feedback
        if word_count < 10:
            complexity_feedback = "Your answer is too short. Try elaborating more."
        elif word_count > 50:
            complexity_feedback = "Your answer is detailed. Make sure it remains concise and relevant."
        else:
            complexity_feedback = "Good balance of detail. Keep refining your structure."

        return f"{sentiment_feedback} {complexity_feedback}"
