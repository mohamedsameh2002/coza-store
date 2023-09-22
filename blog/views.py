from django.shortcuts import render
from .models import Blog,Category,Tags
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q


# Create your views here.


def BLOG (request):
    blogs=Blog.objects.filter(status=True).order_by('-published_at')
    categoriys=Category.objects.all()
    tags=Tags.objects.distinct().values('tag')[:6]
    context={
        'blogs':blogs,
        'categoriys':categoriys,
        'tags':tags,
    }
    return render(request,'blog/blog.html',context)


def BLOG_DETAIL (request,slug,id):
    blog=Blog.objects.get(slug=slug,id=id)
    categoriys=Category.objects.all()
    tags=Tags.objects.distinct().values('tag')[:6]
    context={
        'blog':blog,
        'categoriys':categoriys,
        'tags':tags,
    }
    return render(request,'blog/blog-detail.html',context)




def SEARCH (request):
    search=request.GET.get('search_qury')
    blogs=Blog.objects.filter(Q(topic__icontains=search) | Q(content__icontains=search) | Q(category__category__icontains=search)).order_by('-published_at')
    blog_search=render_to_string('blog/ajax/blog-ajax.html',{'blogs':blogs})
    data={
        'blog_search':blog_search,
    }
    return JsonResponse(data)


def OTHER_IDENTIFIERS (request):
    button=request.GET.get('button')
    text=request.GET.get('text')

    if button == 'category':
        blogs=Blog.objects.filter(category__category=text).order_by('-published_at')
    elif button == 'tags':
        blogs=Blog.objects.filter(tags__tag=text).order_by('-published_at')
        # blogs=Blog.objects.filter(category__category=text).order_by('-published_at')

    blog_otheid=render_to_string('blog/ajax/blog-ajax.html',{'blogs':blogs})
    data={
        'blog_otheid':blog_otheid,
    }
    return JsonResponse(data)
