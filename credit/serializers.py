from rest_framework import serializers
from .models import Borrower, Blacklist, Program, StatusTypes, Application
from .validate import IinGeneration

class RequestIinSerializer(serializers.Serializer):
    iin = serializers.CharField(max_length=12)
    summa = serializers.IntegerField(default=0)


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('summa', 'status', 'rejection_reason', 'program', 'borrower')
        read_only_fields = ['status', 'rejection_reason']

    def create(self, validated_data):
        print(1111111111111111111111111111111)
        print(validated_data)

class BorrowerSerializer(serializers.Serializer):
    iin = serializers.CharField(max_length=12)
    date_of_birth = serializers.DateField()

    def create(self, validated_data):
        print(validated_data)
        return Borrower.objects.create(**validated_data)