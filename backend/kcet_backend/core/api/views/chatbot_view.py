import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from core.models import ChatLog
from core.services.chatbot import (
    answer_using_database,
    groq_answer,
    extract_entities
)

class KCETChatbotView(APIView):
    """
    POST /api/chatbot/
    Body: {"message": "user question"}
    """

    authentication_classes = []
    permission_classes = []

    def log_chat(self, user_question, bot_answer, entities):
        try:
            ChatLog.objects.create(
                user_question=user_question,
                bot_answer=bot_answer or "",
                intent=entities.get("category", ""),
                entities=entities
            )
        except Exception:
            pass  # Logging must never break chatbot

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        data = request.data if isinstance(request.data, dict) else {}
        user_message = data.get("message")

        if not user_message or not user_message.strip():
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        groq_key = os.getenv("GROQ_API_KEY")

        # 1️⃣ Extract structured intent
        entities = extract_entities(user_message)

        # 2️⃣ Query Database first
        db_answer = answer_using_database(user_message)

        final_reply = db_answer["text"]
        source = "database"

        # 3️⃣ Use LLM to rewrite into user-friendly language
        if groq_key:
            system_prompt = (
                "You are a helpful KCET admission assistant. "
                "Rewrite the database answer into a clear, short, actionable response. "
                "If colleges are mentioned, highlight them."
            )

            user_payload = f"User question: {user_message}\n\nDatabase summary:\n{final_reply}"

            try:
                rewritten = groq_answer(system_prompt, user_payload)
                if rewritten:
                    final_reply = rewritten
                    source = "llm+database"
            except Exception:
                pass

        # 4️⃣ Log conversation
        self.log_chat(user_message, final_reply, entities)

        return Response(
            {
                "reply": final_reply,
                "source": source,
                "entities": entities,
                "details": db_answer.get("details", {})
            },
            status=200
        )
