from django.db import models

class Reservation(models.Model):

  class RoomOptions(models.TextChoices):
    A = 'Sala 1'
    B = 'Sala 2'
    C = 'Sala 3'
    D = 'Sala 4'
    E = 'Sala 5'
    F = 'Sala 6'
    G = 'Sala 7'

  class HourOptions(models.TextChoices):
    Nueve = '09'
    Diez = '10'
    Once = '11'
    Doce = '12'
    Trece = '13'
    Catorce = '14'
    Quince = '15'
    Dieciseis = '16'
    Diecisiete = '17'
    Dieciocho = '18'
  
  room = models.CharField(max_length=6, choices=RoomOptions)
  date = models.DateField()
  hour = models.TimeField(choices=HourOptions)
  user = models.TextField(blank=True)

  def __str__(self):
    return {self.room, self.date, self.hour, self.user}

