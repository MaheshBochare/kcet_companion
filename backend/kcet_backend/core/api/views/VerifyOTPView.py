import models 


from models import UserSession

UserSession.objects.create(
    user=user,
    session_id=session_id,
    device=request.META.get("HTTP_USER_AGENT", "")
)
