from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed,JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Tag,Blog

def blog(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            return show_blog(request, request.GET['id'])
        else:
            return list_blogs(request)
    elif request.method == 'POST':
        if 'id' in request.POST:
            return update_blog(request)
        else:
            return create_blog(request)
    else:
        raise HttpResponseBadRequest()

def list_blogs(request):
    tags = []
    if 'tagId' in request.GET:
        blogs = Blog.objects.filter(user__id=userId)
    else:
        if 'userId' in request.GET:
            userId = request.GET['userId']
            blogs = Blog.objects.filter(user__id=userId)
            tags = Tag.objects.filter(user__id=userId)
        elif request.user.is_authenticated():
            userId = request.user.id
            blogs = Blog.objects.filter(user__id=userId)
            tags = Tag.objects.filter(user=request.user)
        else:
            blogs = Blog.objects.all()
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    blogs = Paginator(blogs.order_by('-updated'), 20).page(page)
    context = {'blogs': blogs}
    return render(request, 'jennyhome/blogs.html', context)

def show_blog(request, blogId):
    blog = Blog.objects.get(id=blogId)
    context = {'blog': blog}
    return render(request, 'jennyhome/blog.html', context)

@login_required
def prepare_blog(request):
    tags = Tag.objects.filter(user = request.user)
    blog = {}
    if 'id' in request.GET:
        blog = Blog.objects.get(id=request.GET['id'])
    context = {'tags': tags, 'blog': blog}
    return render(request, 'jennyhome/prepare.html', context)

def create_blog(request):
    blog = Blog(
            user = request.user,
            title = request.POST['title'],
            tags = request.POST['tags'],
            content = request.POST['content']
            )
    blog.save()
    return JsonResponse({'id': blog.id})

def update_blog(request):
    blog = Blog.objects.get(id=request.POST['id'])
    blog.title = request.POST['title']
    blog.content = request.POST['content']
    return JsonResponse({'updated': True})

@login_required
def del_blog(request):
    blog = Blog.objects.get(id=request.GET['id'])
    if blog.user == request.user:
        blog.delete()
        return JsonResponse({})
    else:
        return HttpResponseNotAllowed('You are not allowed to delete this blog')

@login_required
def tag(request):
    if request.method == 'GET':
        return list_tags(request)
    elif request.method == 'POST':
        return update_tag(request)
    else:
        raise HttpResponseBadRequest()

def list_tags(request):
    tags = Tag.objects.all()
    return JsonResponse({})

def update_tag(request):
    tag = Tag(user = request.user,
            name = request.POST['name'])
    tag.save()
    return JsonResponse({})

@login_required
def del_tag(request):
    Tag.objects.filter(name=request.POST['name'], user=request.user).delete()
    return JsonResponse({})
