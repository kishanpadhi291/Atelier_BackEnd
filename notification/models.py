from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
# Create your models here.
class Notification(models.Model):
    notification=models.CharField(max_length=200)
    icon = models.ImageField(upload_to='icons/', storage=MediaCloudinaryStorage(), blank=True, max_length=1000)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    buttonMessage=models.CharField(max_length=50)
    url=models.CharField(max_length=500)

    def __str__(self):
        return f"{self.title}"