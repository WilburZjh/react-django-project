from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):

    # 如果继承的是serializer.Serializer，则需要显式的声明每一个Field。
    # title = serializers.CharField(max_length=120)
    # description = serializers.CharField()
    # completed = serializers.BooleanField(default=False)

    # 因为继承的是ModelSerialzier，则需要定义Meta.
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')

