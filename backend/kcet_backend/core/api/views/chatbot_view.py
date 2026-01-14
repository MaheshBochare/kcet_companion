from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import ChatLog
from core.services.chatbot import (
    chatbot_engine,
    extract_entities
)

class KCETChatbotView(APIView):
    authentication_classes = []
    permission_classes = []

    # -----------------------------
    # Save conversation in DB
    # -----------------------------
    def log_chat(self, user_question, bot_answer, entities, source):
        try:
            ChatLog.objects.create(
                user_question=user_question,
                bot_answer=bot_answer or "",
                intent=source,
                entities=entities
            )
        except Exception:
            pass

    # -----------------------------
    # Main Chat Endpoint
    # -----------------------------
    def post(self, request, *args, **kwargs):

        data = request.data if isinstance(request.data, dict) else {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return Response(
                {"error": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract entities before processing (for logging)
        entities = extract_entities(user_message)

        # 🔮 Hybrid AI engine handles routing + memory + fuzzy + DB + RAG
        result = chatbot_engine(user_message, request)

        reply   = result.get("reply", "No response generated.")
        source  = result.get("source", "unknown")
        details = result.get("details", {})
        confidence = result.get("confidence", 0.0)

        # Store chat safely
        self.log_chat(user_message, reply, entities, source)

        return Response(
            {
                "reply": reply,
                "source": source,
                "entities": entities,
                "details": details,
                "confidence": confidence
            },
            status=status.HTTP_200_OK
        )
