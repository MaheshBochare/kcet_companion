#from django.db import models
from django.db import models
class ChatLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user_question = models.TextField()
    bot_answer = models.TextField(blank=True, null=True)
    intent = models.CharField(max_length=50, blank=True, null=True)
    entities = models.JSONField(default=dict)

    class Meta:
        db_table = "chat_logs"
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["intent"]),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.intent}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "subscribers"

    def __str__(self):
        status = "Approved" if self.is_approved else "Pending"
        return f"{self.email} ({status})"


class ApprovedGmail(models.Model):
    email = models.EmailField(unique=True)
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = "approved_gmails"

    def __str__(self):
        return self.email
