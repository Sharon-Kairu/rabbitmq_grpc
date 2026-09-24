from django.db import models

class Doctor(models.MOdel):
    name=models.CharField(max_length=100)
    speciality=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="bookings")
    patient_name = models.CharField(max_length=100)
    slot_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} with Dr. {self.doctor.name} at {self.slot_time}"