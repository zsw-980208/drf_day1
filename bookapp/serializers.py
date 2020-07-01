from rest_framework import serializers, exceptions

from bookapp.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name", "address", "pic")


class BookModelSerializer(serializers.ModelSerializer):
    publish = PressModelSerializer()
    class Meta:
        model = Book
        # fields = ("book_name", "price", "pic", "publish_name", "press_address", "author_list", "publish")
        fields = ("book_name", "price", "pic", "publish")

        # 可以直接查询所有字段
        # fields = "__all__"

        # 可以指定不展示哪些字段
        # exclude = ("is_delete", "create_time", "status")

        # 指定查询深度  关联对象的查询  可以查询出有外键关系的信息
        # depth = 1

#反序列化器
class BookDeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors")
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 3,  # 最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "长度不够，太短啦~"
                }
            },
            "price": {
                "max_digits": 5,
                "decimal_places": 4,
            }
        }

    def validate_book_name(self, value):
        # 自定义用户名校验规则
        if "1" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        return value

    def validate(self, attrs):
        pwd = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        if pwd != re_pwd:
            raise exceptions.ValidationError("两次密码不一致")

        return attrs

class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # print(type(self))  # 当前调用序列化器类
        # print(instance)  # 要修改的对象
        print(validated_data)   # 要修改的数据
        # print(type(self.child))

        # TODO 将群改 改变成一次改一个  遍历修改
        for index, obj in enumerate(instance):
            # 每遍历一次 就修改一个对象的数据
            self.child.update(obj, validated_data[index])

        return instance


class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields应该填写哪些字段  应该填写序列化与反序列化字段的并集
        fields = ("book_name", "price", "publish", "authors", "pic")

        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 3,  # 最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "长度不够，太短啦~"
                }
            },
            # 指定此字段只参与反序列化
            "publish": {
                "write_only": True
            },
            "authors": {
                "write_only": True
            },
            # 指定某个字段只参与序列化
            "pic": {
                "read_only": True
            }
        }

    def validate_book_name(self, value):
        # 自定义用户名校验规则
        if "1" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        return value

    def validate(self, attrs):

        price = attrs.get("price", 0)
        # 没有获取到 price  所以是 NoneType
        if price > 90:
            raise exceptions.ValidationError("超过设定的最高价钱~")

        return attrs
