from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets, status
from .models import Borrower, Blacklist, Application, Program, StatusTypes
from .serializers import RequestIinSerializer, ApplicationSerializer, BorrowerSerializer
from .validate import check_iin_generation, IinGeneration, checkapp

class IinView(GenericAPIView):
    serializer_class = RequestIinSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        check_iin = check_iin_generation(data['iin'])
        date_of_birth = IinGeneration(data['iin']).date_of_birth()
        if check_iin == StatusTypes.approved and date_of_birth[0] == StatusTypes.approved:
            borrower, _ = Borrower.objects.get_or_create(iin=data['iin'], date_birth=date_of_birth[1])
            app = checkapp(borrower, data['summa'])
            if app[0] == StatusTypes.approved:
                return Response(StatusTypes.approved, status=status.HTTP_200_OK)
            else:
                return Response(StatusTypes.denied, status=status.HTTP_400_BAD_REQUEST)
        return Response(date_of_birth[1], status=status.HTTP_200_OK)



class ApplicationView(GenericAPIView):
    serializer_class = ApplicationSerializer
    def post(self, request):
        print(22222222222222)

class BorrowerView(GenericAPIView):
    serializer_class = BorrowerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response({'key': 'value'}, status=status.HTTP_200_OK)
