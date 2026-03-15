from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Module(models.Model):
    class Level(models.TextChoices):
        CP1 = '1CP', '1CP'
        CP2 = '2CP', '2CP'
        CS1 = '1CS', '1CS'
        CS2 = '2CS', '2CS'
        CS3 = '3CS', '3CS'

    class Semester(models.TextChoices):
        S1 = 'S1', 'Semester 1'
        S2 = 'S2', 'Semester 2'

    name     = models.CharField(max_length=100)
    level    = models.CharField(max_length=5, choices=Level.choices)
    semester = models.CharField(max_length=2, choices=Semester.choices)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'level', 'semester']

    def __str__(self):
        return f"{self.name} ({self.level} - {self.semester})"


class Resource(models.Model):
    class ResourceType(models.TextChoices):
        COUR     = 'COUR',     'Cours'
        TD       = 'TD',       'TD'
        TP       = 'TP',       'TP'
        EXAM     = 'EXAM',     'Exam'
        INTERRO  = 'INTERRO',  'Interro'
        OTHER    = 'OTHER',    'Other'

    title         = models.CharField(max_length=255)
    module        = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='resources')
    uploaded_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resources')
    resource_type = models.CharField(max_length=10, choices=ResourceType.choices)
    academic_year = models.PositiveIntegerField()
    file          = models.FileField(upload_to='temp_uploads/', null=True, blank=True)
    file_hash     = models.CharField(max_length=64, unique=True)
    drive_id      = models.CharField(max_length=255, null=True, blank=True)
    downloads     = models.PositiveIntegerField(default=0)
    is_verified   = models.BooleanField(default=False)
    uploaded_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def get_drive_url(self):
        if self.drive_id:
            return f"https://drive.google.com/file/d/{self.drive_id}/view"
        return None

    def get_download_url(self):
        if self.drive_id:
            return f"https://drive.google.com/uc?export=download&id={self.drive_id}"
        return None
