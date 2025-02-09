from datetime import timezone

from django.db import models
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(max_length=200)
    title2 = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='blog/')
    created_at = models.DateTimeField()
    content = models.TextField()
    content2 = models.TextField(blank=True, null=True)
    timeread = models.CharField(max_length=200)
    views = models.PositiveIntegerField(default=0)
    blockquote = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('blog_detail', args=[str(self.id)])
