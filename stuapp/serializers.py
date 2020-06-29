from rest_framework import serializers
from drf_day1 import settings
from stuapp.models import Student


class StudentSerializer(serializers.Serializer):
    name = serializers.CharField()
    age=serializers.IntegerField()
    gender = serializers.IntegerField()
    pic = serializers.ImageField()
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
class StudentDeSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=4,
        min_length=2,
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了",
        }
    )
    age=serializers.IntegerField()
    phone = serializers.CharField()
    def create(self, validated_data):
        return Student.objects.create(**validated_data)
