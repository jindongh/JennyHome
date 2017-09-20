# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import json
from .models import Gallery, Photo, Comment
from .forms import PhotoForm, GalleryForm

# Create your views here.
def home(request):
    galleryList = Gallery.objects.all()
    return render(request, 'baby/home.html', {'galleryList': galleryList})

def showGallery(request, galleryId):
    gallery = Gallery.objects.get(pk=galleryId)
    return render(request, 'baby/gallery.html', {'gallery': gallery})

def addGallery(request):
    if request.method == 'GET':
        form = GalleryForm()
    else:
        form = GalleryForm(request.POST)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.user = request.user
            gallery.save()
            return redirect(home)

    return render(request, 'baby/addGallery.html', {'form': form})

def listPhotos(request, galleryId):
    photos = Photo.objects.filter(gallery__id=galleryId)
    return JsonResponse([{
        'id': photo.id,
        'description': photo.description,
        'created': photo.created,
        'url': _photoUrl(photo.id),
        } for photo in photos], safe = False)

def deletePhoto(request, photoId):
    photo = Photo.objects.get(pk=photoId)
    if photo is None:
        raise Http404
    elif photo.gallery.user != request.user:
        return HttpResponseForbidden()
    else:
        photo.delete()
        return JsonResponse({})

def getImage(request, photoId):
    photo = Photo.objects.get(pk=photoId)
    image = photo.image.read()
    return HttpResponse(
            image, content_type='image/jpeg'
            )

def uploadPhoto(request, galleryId):
    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({
            'succeed': False,
            'message': json.dumps(form.errors, indent=4),
            })
    photo = form.save(commit=False)
    photo.gallery = Gallery.objects.get(pk=galleryId)
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
    return reverse(getImage, args=(photoId,))
