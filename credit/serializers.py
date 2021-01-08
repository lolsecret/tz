from rest_framework import serializers
from .models import Borrower, Application


class RequestIinSerializer(serializers.Serializer):
    iin = serializers.CharField(max_length=12)
    summa = serializers.IntegerField(default=0)