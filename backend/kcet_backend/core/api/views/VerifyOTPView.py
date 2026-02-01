
from django.http import JsonResponse

response = JsonResponse({
    "message": "Login successful",
    "role": user.role,
})

response.set_cookie(
    key="access_token",
    value=str(refresh.access_token),
    httponly=True,
    secure=True,      # True in production
    samesite="Lax",
    max_age=900,
)

response.set_cookie(
    key="refresh_token",
    value=str(refresh),
    httponly=True,
    secure=True,
    samesite="Lax",
    max_age=86400,
)
return response
