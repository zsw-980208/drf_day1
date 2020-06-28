from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from userapp.models import User


@method_decorator(csrf_exempt, name="dispatch")  # 让类视图免除csrf认证
class UserView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        if user_id:  # 查询单个
            user_val = User.objects.filter(pk=user_id).values("username", "password", "gender").first()
            if user_val:
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user_val
                })
        else:
            # 如果没有传参数id  代表查询所有
            user_list = User.objects.all().values("username", "password", "gender")
            print(type(user_list))
            if user_list:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_list),
                })
        return JsonResponse({
            "status": 500,
            "message": "查询失败",
        })

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        try:
            user_obj = User.objects.create(username=username, password=pwd)
            return JsonResponse({
                "status": 201,
                "message": "创建用户成功",
                "results": {"username": user_obj.username, "gender": user_obj.gender}
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建用户失败",
            })

    def put(self, request, *args, **kwargs):
        print("PUT SUCCESS  修改")
        return HttpResponse("PUT SUCCESS")

    def delete(self, request, *args, **kwargs):
        print("DELETE SUCCESS  删除")
        return HttpResponse("DELETE SUCCESS")


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        if user_id:  # 查询单个
            user_val = User.objects.filter(pk=user_id).values("username", "password", "gender").first()
            if user_val:
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user_val
                })
        else:
            # 如果没有传参数id  代表查询所有
            user_list = User.objects.all().values("username", "password", "gender")
            print(type(user_list))
            if user_list:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_list),
                })

        return JsonResponse({
            "status": 500,
            "message": "查询失败",
        })

    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response("POST GET SUCCESS")
