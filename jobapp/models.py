from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    image = models.ImageField()

    def __str__(self):
        return self.title
# Create your models here.
