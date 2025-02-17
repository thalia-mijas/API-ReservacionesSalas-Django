from rest_framework import serializers
from .models import Reservation
from rest_framework.validators import UniqueTogetherValidator

class ReservationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reservation
    fields = ['id', 'room', 'date', 'hour', 'user']
    validators = [
      UniqueTogetherValidator(
        queryset=Reservation.objects.all(),
        fields=['room', 'date', 'hour']
      )
    ]