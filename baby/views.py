# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import Photo, Comment
from .forms import PhotoForm

# Create your views here.
def home(request):
    return render(request, 'baby/home.html')

def listPhotos(request):
    photos = Photo.objects.all()
    return JsonResponse([{
        'id': photo.id,
        'description': photo.description,
        'created': photo.created,
        'url': _photoUrl(photo.id),
        } for photo in photos], safe = False)

def getImage(request, photoId):
    photo = Photo.objects.get(pk=photoId)
    image = photo.image.read()
    return HttpResponse(
            image, content_type='image/jpeg'
            )

def uploadPhoto(request):
    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({
            'succeed': False,
            'message': json.dumps(form.errors, indent=4),
            })
    photo = form.save(commit = False)
    photo.user = request.user
    photo.save()
    return JsonResponse({
        'succeed': True,
        'photo': {
            'id': photo.id,
            'url': _photoUrl(photo.id),
            'description': photo.description,
            },
        })

def listComments(request):
    photoId = request.GET['photoId']
    comments = Comment.objects.filter(photo__id=photoId)
    return JsonResponse([{
        'user': comment.user,
        'created': comment.created,
        'content': comment.content,
        } for comment in comments
        ], safe = False)

@login_required
def addComment(request):
    comment = Comment(
            user = request.user,
            content = request.POST['content'])
    comment.save()
    return JsonResponse({
        'succeed': True,
        'id': comment.id,
        'message': 'succeed',
        })

def deleteComment(request):
    pass

def _photoUrl(photoId):
    return 'api/image/%d' % photoId
