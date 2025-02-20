import requests
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Reservation
from .serializers import ReservationSerializer
import datetime
from rest_framework.permissions import DjangoModelPermissions

class ReservationViewSet(viewsets.ModelViewSet):
  queryset = Reservation.objects.all()
  serializer_class = ReservationSerializer
  permission_classes = [DjangoModelPermissions]

  def destroy(self, request, pk=None):
    try:
      reservation = Reservation.objects.get(pk=pk)
      reservation.delete()
      return Response({'detail': 'Reservation eliminaded'}, status=status.HTTP_200_OK)
    except Reservation.DoesNotExist:
      return Response({'detail': 'Reservation does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
  def create(self, request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
      if (serializer.validated_data['date'] < datetime.date.today()) or (serializer.validated_data['date'] == datetime.date.today() and int(serializer.validated_data['hour']) <= datetime.datetime.now().hour):
        return Response({'detail': 'Date or time no longer available'}, status=status.HTTP_400_BAD_REQUEST)
      else:
        if request.user.is_staff:
          if serializer.validated_data['user'] == "":
            serializer.validated_data['user'] = request.user
        else:
          serializer.validated_data['user'] = request.user
        serializer.save()
        return Response(serializer.data)    
    return Response(serializer.errors)
  
  def update(self, request, pk=None):
    try:
      reservation = Reservation.objects.get(pk=pk)
      serializer = ReservationSerializer(data=request.data)
      if serializer.is_valid():
        if (serializer.validated_data['date'] < datetime.date.today()) or (serializer.validated_data['date'] == datetime.date.today() and int(serializer.validated_data['hour']) <= datetime.datetime.now().hour):
          return Response({'detail': 'Date or time no longer available'}, status=status.HTTP_400_BAD_REQUEST)
        else:
          reservation.room = serializer.data['room']
          reservation.date = serializer.data['date']
          reservation.hour = serializer.data['hour']
          if request.user.is_staff:
            if serializer.validated_data['user'] == "":
              serializer.validated_data['user'] = request.user
          else:
            serializer.validated_data['user'] = request.user
          serializer.save()
          return Response(serializer.data)      
      return Response(serializer.errors)
    except Reservation.DoesNotExist:
      return Response({'detail': 'Reservation does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request, pk=None):
    if request.user.is_staff:
      reservations = Reservation.objects.all().order_by('-date', '-hour')
    else:
      reservations = Reservation.objects.filter(user=request.user).values().order_by('-date', '-hour')
      if pk != None:
        reservations = reservations.filter(id=pk).values()
        serializer = ReservationSerializer(reservations, many=False)
        return Response(serializer.data)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk=None):
    try:
      reservation = Reservation.objects.get(pk=pk)
      if request.user.is_staff:
        return Response(reservation)
      else:
        return Response({'detail': 'Acceso denegado'}, status=status.HTTP_401_UNAUTHORIZED)
    except Reservation.DoesNotExist:
      return Response({'detail': 'Reservation does not exist'}, status=status.HTTP_404_NOT_FOUND)
  
