from rest_framework import serializers
from core.models import College, Branch, Cutoff, SeatMatrix, Category

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

class CutoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cutoff
        fields = "__all__"

class SeatMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatMatrix
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
from core.models import Subscriber

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"
from core.models import ChatLog

class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = "__all__"
