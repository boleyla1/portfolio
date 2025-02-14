from django.shortcuts import render, get_object_or_404
from .models import Blog
import jdatetime
from django.utils.text import slugify


def blog_list(request):
    blogs = Blog.objects.all()

    # بررسی و مقداردهی اولیه اسلاگ
    for blog in blogs:
        if not blog.slug:
            blog.slug = slugify(blog.title, allow_unicode=True)
            blog.save()
        # تبدیل تاریخ میلادی به شمسی
        blog.created_at_shamsi = jdatetime.datetime.fromgregorian(datetime=blog.created_at).strftime('%Y/%m/%d %H:%M')

    return render(request, 'weblog/blog.html', {'blogs': blogs})


def blog_detail(request, slug):
    # جستجوی مقاله با استفاده از اسلاگ
    blog = get_object_or_404(Blog, slug=slug)

    # افزایش تعداد بازدیدها
    blog.views += 1
    blog.save()

    # تبدیل تاریخ میلادی به شمسی
    blog.created_at_shamsi = jdatetime.datetime.fromgregorian(datetime=blog.created_at).strftime('%Y/%m/%d %H:%M')

    return render(request, 'weblog/blog_details.html', {'blog': blog})
