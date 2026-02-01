from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsAdmin, IsOwner
from core.models import User

class SystemSettingsView(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        return Response({
            "message": "Owner-level system access granted"
        })


class ApprovedGmailView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        user.is_approved = True
        user.save()

        return Response({
            "message": f"{email} approved successfully"
        })
