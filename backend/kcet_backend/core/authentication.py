from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class SingleSessionJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("access_token")
        if not token:
            return None

        validated = self.get_validated_token(token)
        user = self.get_user(validated)

        if str(user.current_session_id) != validated.get("session_id"):
            raise AuthenticationFailed("Logged in elsewhere")

        return user, validated
