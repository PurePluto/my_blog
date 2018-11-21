from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Blog, Category
from read_statistics.utils import read_statistics_once_read



def get_blog_list_common_date(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, 10)  # 分页，每页10条数据
    page_num = request.GET.get('page', 1)  # 获取url的页面参数
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页面的前后各两页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略符号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 按照日期分类
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                         create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = Category.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_date(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_type(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    blogs_all_list = Blog.objects.filter(category=category)
    context = get_blog_list_common_date(request, blogs_all_list)
    context['category'] = category
    return render(request, 'blog/blog_type.html', context)


def blog_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = get_blog_list_common_date(request, blogs_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blog_date.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, id=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    context = {}
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['blog'] = blog
    response = render(request, 'blog/blog_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response
