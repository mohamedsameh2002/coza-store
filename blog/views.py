import secrets
from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog,Category,Comments,Reply,Notification
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models.functions import ExtractYear
from .forms import CommentsForm,ReplyForm
from accounts.models import UserProfile
from taggit.models import Tag
from django.contrib import messages

# Create your views here.


def BLOG (request,tag_slug=None):
    blogs=Blog.objects.filter(status=True).order_by('-published_at')
    notifs=Notification.objects.filter(reply_recipient=request.user).exclude(reply_sent=request.user)
    is_news=Notification.objects.filter(reply_recipient=request.user,seen=False).exclude(reply_sent=request.user).exists()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        blogs=blogs.filter(tags__in=[tag])
    paginator = Paginator(blogs, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    categoriys=Category.objects.all()

    archive = Blog.objects.annotate(year=ExtractYear('published_at')).values('year').distinct()
    tags=Tag.objects.all().order_by('-created_date')
    context={
        'blogs':page_obj,
        'categoriys':categoriys,
        'archive':archive,
        'tag':tag,
        'tags':tags,
        'notifs':notifs,
        'is_news':is_news,
    }
    return render(request,'blog/blog.html',context)


def hide_noti_icon(request):
    notifs=Notification.objects.filter(reply_recipient=request.user)
    if Notification.objects.filter(reply_recipient=request.user).exists():
        for i in notifs:
            i.seen=True
        i.save()
    return JsonResponse({})



def BLOG_DETAIL (request,slug,id):
    blog=Blog.objects.get(slug=slug,id=id)
    categoriys=Category.objects.all()
    userprofile=UserProfile.objects.get(user=request.user)
    try:
        comments=Comments.objects.filter(post=blog).order_by('-created_date')[:4]
    except:
        comments=None
    archive = Blog.objects.annotate(year=ExtractYear('published_at')).values('year').distinct()
    tags=Tag.objects.all()
    context={
        'blog':blog,
        'categoriys':categoriys,
        'archive':archive,
        'comments':comments,
        'userprofile':userprofile,
        'tags':tags,
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


def ADD_COMMENT(request):
    slug=request.POST.get('slug')
    id=request.POST.get('id')
    post=Blog.objects.get(slug=slug,id=id)
    comment = request.POST.get('formData', '').split('=')[1]
    userprofile=UserProfile.objects.get(user=request.user)
    inf={'comment':comment}
    commentform=CommentsForm(inf)
    if commentform.is_valid():
        save=commentform.save(commit=False)
        save.post=post
        save.user=userprofile
        save.save()
    else:
        print('nooooooooooo')
    comments=Comments.objects.filter(post=post).order_by('-created_date')
    context={
        'comments':comments,
        'userprofile':userprofile,
        'id':id,
        'slug':slug,
        }

    template=render_to_string('blog/ajax/comments.html',context)
    comments_count=post.commetns_count()
    data={'template':template,'comments_count':comments_count}
    return JsonResponse(data)



def ADD_REPLY(request):
    val=request.GET['val']
    reply=request.GET['reply']
    post_id=request.GET['id']
    slug=request.GET['slug']
    post=Blog.objects.get(id=post_id,slug=slug)
    comment_id=request.GET['comment_id']
    userprofile=UserProfile.objects.get(user=request.user)
    comment=Comments.objects.get(id=comment_id)
    reply_form=ReplyForm({'reply':reply})
    if reply_form.is_valid():
        save=reply_form.save(commit=False)
        save.reply=reply
        save.user=userprofile
        save.post=post
        if val == 'reply4comment':
            save.comment=comment
            Notification.objects.create(post=post,
            reply_sent=request.user,
            reply_recipient=comment.user.user,
            comment=comment,
            )
        else:
            reply_id=request.GET['reply_id']
            reply4reply=Reply.objects.get(id=reply_id)
            save.parent_reply=reply4reply
            save.comment=comment
            Notification.objects.create(post=post,
            reply_sent=request.user,
            reply_recipient=reply4reply.user.user,
            comment=comment,
            reply=reply4reply,
            )
        save.save()
    replyes=Reply.objects.filter(comment=comment)
    random_1 = secrets.token_hex(4).title().swapcase()
    template=render_to_string('blog/ajax/replys.html',{'replyes':replyes,'userprofile':userprofile,'random_1':random_1})
    count=comment.count_reply()
    comments_count=post.commetns_count()
    data={'template':template,'count':count,'comments_count':comments_count}
    return JsonResponse(data)


def DELET_COM_Rep(request,id,val):
    if val == 'comment':
        Comments.objects.get(id=id).delete()
    else:
        Reply.objects.get(id=id).delete()
    url=request.META.get('HTTP_REFERER')
    if '/en/' in request.path:
        messages.success(request,'Your comment has been successfully deleted')
    else:
        messages.success(request,'تم حذف تعليقك بنجاح')
    return redirect(url)



def LOAD_COMMENTS(request):
    page=int( request.GET.get('page'))
    lent=int( request.GET.get('lent'))
    id=request.GET['id']
    slug=request.GET['slug']
    userprofile=UserProfile.objects.get(user=request.user)
    blog=Blog.objects.get(slug=slug,id=id)
    comments=Comments.objects.filter(post=blog).order_by('-created_date')[lent:lent+page]
    count=Comments.objects.filter(post=blog).count()
    random_1_fvort = secrets.token_hex(4).title().swapcase()
    random_2_qick = secrets.token_hex(4).title().swapcase()
    random_3_addmodal = secrets.token_hex(4).title().swapcase()
    random_4_select_size = secrets.token_hex(4).title().swapcase()
    context={
        'comments':comments,
        'userprofile':userprofile,
        'id':id,
        'slug':slug,
        'random_1_fvort':random_1_fvort,
        'random_2_qick':random_2_qick,
        'random_3_addmodal':random_3_addmodal,
        'random_4_select_size':random_4_select_size,
        }
    html=render_to_string('blog/ajax/load_comments.html',context)
    data={'count':count,'html':html}
    return JsonResponse(data)