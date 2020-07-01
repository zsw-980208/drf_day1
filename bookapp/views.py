from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from bookapp.models import Book
from .serializers import BookModelSerializer, BookDeModelSerializer, BookModelSerializerV2, BookListSerializer


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:

            book_obj = Book.objects.get(pk=book_id)
            book_ser = BookModelSerializer(book_obj).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询单个图书成功",
                "results": book_ser
            })

        else:
            book_list = Book.objects.all()
            book_list_ser = BookModelSerializer(book_list, many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询所有图书成功",
                "results": book_list_ser
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        book_ser = BookDeModelSerializer(data=request_data)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            "result": BookModelSerializer(book_obj).data
        })


class BookAPIViewV2(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:

            book_obj = Book.objects.filter(pk=book_id, is_delete=False)
            book_ser = BookModelSerializerV2(book_obj).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询单个图书成功",
                "results": book_ser
            })

        else:
            book_list = Book.objects.filter(is_delete=False)
            book_list_ser = BookModelSerializerV2(book_list, many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询所有图书成功",
                "results": book_list_ser
            })

    def post(self, request, *args, **kwargs):
        """
        增加单个：传递参数的格式 字典
        增加多个：[{},{},{}]  列表中嵌套的事一个个的图书对象
        """
        request_data = request.data
        if isinstance(request_data, dict):  # 增加单个图书
            many = False
        elif isinstance(request_data, list):  # 增加多个图书
            many = True
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "请求参数格式有误",
            })

        book_ser = BookModelSerializerV2(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            "result": BookModelSerializerV2(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败或图书不存在"
        })

    def put(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })
        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializerV2(book_obj).data
        })

    # def patch(self, request, *args, **kwargs):
    #     request_data = request.data
    #     book_id = kwargs.get("id")
    #
    #     try:
    #         book_obj = Book.objects.get(pk=book_id)
    #     except:
    #         return Response({
    #             "status": status.HTTP_400_BAD_REQUEST,
    #             "message": "图书不存在"
    #         })
    #     book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
    #     book_ser.is_valid(raise_exception=True)
    #
    #     book_ser.save()
    #
    #     return Response({
    #         "status": status.HTTP_400_BAD_REQUEST,
    #         "message": "更新成功",
    #         "results": BookModelSerializerV2(book_obj).data
    #     })

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        if book_id and isinstance(request_data, dict):
            book_ids = [book_id, ]
            request_data = [request_data]
        elif not book_id and isinstance(request_data, list):
            book_ids = []
            for dic in request_data:
                pk = dic.pop("pk", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "PK不存在",
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "数据格式有误",
            })
        book_list = []
        new_data = []
        for index, pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])
                # print(request_data[index])
            except:
                # 如果图书对象不存在  则将id与对应数据都移除
                # index = book_ids.index(pk)
                # request_data.pop(index)
                continue

        book_ser = BookListSerializer(data=new_data, instance=book_list, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "修改成功",
        })