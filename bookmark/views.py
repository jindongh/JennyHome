# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Bookmark

# Create your views here.
def home(request):
    categories = Category.objects.filter(user=_getUser(request))
    return render(request, 'bookmark/home.html', { 'categories': categories })

def list_bookmark(request, categoryId):
    if categoryId == '-1':
        bookmarks = Bookmark.objects.filter(user=_getUser(request)).order_by('-click')[:10]
    else:
        bookmarks = Bookmark.objects.filter(category = Category.objects.get(pk=categoryId))
    return JsonResponse([_bookmark2Json(bookmark) for bookmark in bookmarks], safe=False)

def edit_category(request):
    name = request.POST['name']
    if 'id' in request.POST and request.POST['id'] != '':
        category = Category.objects.get(pk=request.POST['id'])
        category.name = name
    else:
        category = Category(
                user = _getUser(request),
                name = name)
    category.save()
    return JsonResponse(_category2Json(category))

def edit_bookmark(request, categoryId):
    category = Category.objects.get(pk=categoryId)
    name = request.POST['name']
    link = request.POST['link']
    if 'id' in request.POST and request.POST['id'] != '':
        bookmark = Bookmark.objects.get(pk=int(request.POST['id']))
        bookmark.name = name
        bookmark.link = link
    else:
        bookmark = Bookmark(
                user = _getUser(request),
                category = category,
                name = name,
                link = link)
    bookmark.save()
    return JsonResponse(_bookmark2Json(bookmark))

def delete_category(request, categoryId):
    category = Category.objects.get(pk=categoryId)
    response = JsonResponse(_category2Json(category))
    category.delete()
    return response

def delete_bookmark(request, bookmarkId):
    bookmark = Bookmark.objects.get(pk=bookmarkId)
    bookmark.delete()
    return JsonResponse(_bookmark2Json(bookmark))

def access_bookmark(request, bookmarkId):
    bookmark = Bookmark.objects.get(pk=bookmarkId)
    bookmark.click += 1
    bookmark.save()
    return redirect(bookmark.link)

def _getUser(request):
    return request.user.is_active and request.user or None

def _category2Json(category):
    return {
            'id': category.id,
            'name': category.name
            }

def _bookmark2Json(bookmark):
    return {
            'id': bookmark.id,
            'category': bookmark.category.id,
            'name': bookmark.name,
            'link': bookmark.link,
            'click': bookmark.click,
            }
