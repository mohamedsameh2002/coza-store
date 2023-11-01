from django.shortcuts import render
from .models import Blog,Category,Tags
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models.functions import ExtractYear

# Create your views here.


def BLOG (request):
    blogs=Blog.objects.filter(status=True).order_by('-published_at')
    paginator = Paginator(blogs, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    categoriys=Category.objects.all()
    all_tags=Tags.objects.all().order_by('-criated_at')
    tags=[]
    tags_ar=[]
    for tag in all_tags:
        if tag.tag not in tags :
            tags.append(tag.tag)
        else:
            continue

    for tag in all_tags:
        if tag.tag_ar not in tags_ar :
            tags_ar.append(tag.tag_ar)
        else:
            continue

    archive = Blog.objects.annotate(year=ExtractYear('published_at')).values('year').distinct()

    context={
        'blogs':page_obj,
        'categoriys':categoriys,
        'tags':tags,
        'tags_ar':tags_ar,
        'archive':archive,
    }
    return render(request,'blog/blog.html',context)


def BLOG_DETAIL (request,slug,id):
    blog=Blog.objects.get(slug=slug,id=id)
    categoriys=Category.objects.all()
    archive = Blog.objects.annotate(year=ExtractYear('published_at')).values('year').distinct()
    all_tags=Tags.objects.all().order_by('-criated_at')
    tags=[]
    tags_ar=[]
    for tag in all_tags:
        if tag.tag not in tags :
            tags.append(tag.tag)
        else:
            continue

    for tag in all_tags:
        if tag.tag_ar not in tags_ar :
            tags_ar.append(tag.tag_ar)
        else:
            continue

    context={
        'blog':blog,
        'categoriys':categoriys,
        'tags':tags,
        'tags_ar':tags_ar,
        'archive':archive,
    }
    return render(request,'blog/blog-detail.html',context)




def SEARCH (request):
    lang=None
    if '/en/' in request.path:
        lang='en'
    else:
        lang='ar'
    search=request.GET.get('search_qury')
    if '/en/' in request.path:
        blogs=Blog.objects.filter(Q(topic__icontains=search) | Q(content__icontains=search) | Q(category__category__icontains=search)).order_by('-published_at')
    else:
        blogs=Blog.objects.filter(Q(topic_ar__icontains=search) | Q(content_ar__icontains=search) | Q(category__category_ar__icontains=search)).order_by('-published_at')

    blog_search=render_to_string('blog/ajax/blog-ajax.html',{'blogs':blogs,'lang':lang})
    data={
        'blog_search':blog_search,
    }
    return JsonResponse(data)


def OTHER_IDENTIFIERS (request):
    button=request.GET.get('button')
    text=request.GET.get('text')

    if '/en/' in request.path:
        lang='en'
    else:
        lang='ar'

    if button == 'category':
        blogs=Blog.objects.filter(category__category=text).order_by('-published_at')
    elif button == 'tags':
        if '/en/' in request.path:
            blogs=Blog.objects.filter(tags__tag=text).order_by('-published_at')
        else:
            blogs=Blog.objects.filter(tags__tag_ar=text).order_by('-published_at')
    elif button == 'archive':
        blogs=Blog.objects.filter(published_at__year=text).order_by('-published_at')

    blog_otheid=render_to_string('blog/ajax/blog-ajax.html',{'blogs':blogs,'lang':lang})
    data={
        'blog_otheid':blog_otheid,
    }
    return JsonResponse(data)
