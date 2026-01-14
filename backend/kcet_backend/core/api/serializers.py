from rest_framework import serializers
from core.models import College, Branch, Cutoff, SeatMatrix, Category
import math

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

class FeaturedCollegeSerializer(serializers.Serializer):
    name = serializers.CharField()
    location = serializers.CharField(allow_blank=True, allow_null=True)
    naac = serializers.CharField(allow_blank=True, allow_null=True)
    highest_package = serializers.FloatField()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # 🧼 sanitize highest_package
        hp = data["highest_package"]
        if hp is None or (isinstance(hp, float) and math.isnan(hp)):
            data["highest_package"] = 0

        # 🧼 sanitize naac
        if not data["naac"]:
            data["naac"] = "N/A"

        return data
from rest_framework import serializers
import math


class FeaturedCollegeSerializer(serializers.Serializer):
    name = serializers.CharField()
    location = serializers.CharField(allow_blank=True, allow_null=True)
    naac = serializers.CharField(allow_blank=True, allow_null=True)
    highest_package = serializers.FloatField()

    def validate_highest_package(self, value):
        if value is None:
            return 0.0
        if isinstance(value, float) and math.isnan(value):
            return 0.0
        if value < 0:
            return 0.0
        return value

    def validate_naac(self, value):
        if not value:
            return "N/A"
        return value

    def validate_location(self, value):
        if not value:
            return "N/A"
        return value
