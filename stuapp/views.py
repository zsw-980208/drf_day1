from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from stuapp.models import Student
from stuapp.serializers import StudentSerializer, StudentDeSerializer


class StudentAPIView(APIView):

    def get(self, request, *args, **kwargs):
        stu_id = kwargs.get("pk")
        if stu_id:
            stu_obj = Student.objects.get(pk=stu_id)
            stu_ser = StudentSerializer(stu_obj)
            data = stu_ser.data
            return Response({
                "status": 200,
                "msg": "查询单个学生成功",
                "results": data,
            })
        else:
            stu_list = Student.objects.all()
            stu_list_ser = StudentSerializer(stu_list, many=True).data
            return Response({
                "status": 200,
                "msg": "查询所有学生成功",
                "results": stu_list_ser,
            })

    def post(self, request, *args, **kwargs):
        stu_data = request.data
        if not isinstance(stu_data, dict) or stu_data == {}:
            return Response({
                "status": 501,
                "msg": "数据有误",
            })
        serializer = StudentDeSerializer(data=stu_data)
        print(serializer.is_valid())
        if serializer.is_valid():
            stu_obj = serializer.save()
            return Response({
                "status": 201,
                "msg": "创建学生成功",
                "results": StudentSerializer(stu_obj).data
            })
        else:
            return Response({
                "status": 501,
                "msg": "创建学生失败",
                "results": serializer.errors
            })
