from datetime import timezone

import jdatetime
from django.db import models
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(max_length=200)
    title2 = models.CharField(max_length=200, blank=True, null=True)
    title3 = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='blog/')
    created_at = models.DateTimeField()
    content = models.TextField(blank=True, null=True)
    content2 = models.TextField(blank=True, null=True)
    content3 = models.TextField(blank=True, null=True)
    timeread = models.CharField(max_length=200)
    views = models.PositiveIntegerField(default=0)
    blockquote = models.TextField(blank=True, null=True)
    about = models.CharField(max_length=100, blank=True, null=True)

    @property
    def created_at_shamsi(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at).strftime('%Y/%m/%d %H:%M')

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('blog_detail', args=[str(self.id)])
    @created_at_shamsi.setter
    def created_at_shamsi(self, value):
        self._created_at_shamsi = value
