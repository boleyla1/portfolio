# views.py
from django.shortcuts import render, get_object_or_404
from .models import Blog
import jdatetime


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'weblog/blog.html', {'blogs': blogs})


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.views += 1
    blog.save()
    blog.created_at_shamsi = jdatetime.datetime.fromgregorian(datetime=blog.created_at).strftime('%Y/%m/%d %H:%M')
    return render(request, 'weblog/blog_details.html', {'blog': blog})
