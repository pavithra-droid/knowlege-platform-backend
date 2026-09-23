from django.db import models
from django.conf import settings
from pgvector.django import VectorField

class Document(models.Model):
    class ProcessingStatus(models.TextChoices):
        PENDING = ("PENDING", "Pending")
        PROCESSING = ("PROCESSING", "Processing")
        COMPLETED = ("COMPLETED", "Completed")
        FAILED = ("FAILED", "Failed")
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=200, choices=ProcessingStatus.choices, default=ProcessingStatus.PENDING)
    files = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extracted_text = models.TextField(blank=True, default="")
    
    def __str__(self):
        return self.title
    
    
class Documentchunk(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks"
    )
    content = models.TextField()
    chunk_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    embedding = VectorField(dimensions=384, null=True)
    
    def __str__(self):
        return f"{self.document.title} - {self.chunk_index}"