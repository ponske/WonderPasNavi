from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Image(models.Model):
    attraction_id = models.CharField(max_length=10, default='default_value')
    image = CloudinaryField('image', null=True)

    def __str__(self):
        return f"{self.attraction_id} image"