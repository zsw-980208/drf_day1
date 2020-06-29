from rest_framework import serializers
from empapp.models import Employee
from drf_day1 import settings

class EmployeeSerializer(serializers.Serializer):
    username = serializers.CharField()
    # password = serializers.CharField()
    gender = serializers.IntegerField()
    pic = serializers.ImageField()
    salt = serializers.SerializerMethodField()
    def get_salt(self, obj):
        return "salt"
    gender = serializers.SerializerMethodField()
    def get_gender(self, obj):
        return obj.get_gender_display()
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        # print(obj.pic)
        # http://127.0.0.1:8000/media/pic/000.jpg
        # print("http://127.0.0.1:8000"+settings.MEDIA_URL + str(obj.pic))

        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, str(obj.pic))


# 反序列化器
class EmployeeDeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=8,
        min_length=2,
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了",
        }
    )
    password = serializers.CharField(required=False)
    phone = serializers.CharField()
    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
