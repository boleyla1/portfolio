import jdatetime
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='projects/')
    company = models.CharField(max_length=100)
    url = models.URLField(max_length=200, default='https://www.google.com')

    def end_date_shamsi(self):
        return jdatetime.datetime.fromgregorian(datetime=self.end_date).strftime('%Y/%m/%d %H:%M')

    def start_date_shamsi(self):
        return jdatetime.datetime.fromgregorian(datetime=self.end_date).strftime('%Y/%m/%d %H:%M')

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='skills/')

    def __str__(self):
        return self.name


class RecentProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=100)
    icon_svg = models.TextField(help_text='Paste SVG code here')

    def __str__(self):
        return self.name
