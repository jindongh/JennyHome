# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.http import Http404
from .models import Note
import logging
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def home(request):
    return render(request, 'note/home.html', {})

@login_required
def get_list(request):
    notes = Note.objects.filter(user=request.user, finished=False).order_by('-date')[:20]
    return JsonResponse([_note2Json(note) for note in notes], safe=False)

@login_required
def get_history(request):
    notes = Note.objects.filter(user=request.user, finished=True).order_by('-date')[:20]
    return JsonResponse([_note2Json(note) for note in notes], safe=False)

@login_required
def add(request):
    logger.info('Add note with request ' + request.body)
    note = Note(user = request.user,
            content = request.POST['content'])
    note.save()
    return JsonResponse(_note2Json(note))

@login_required
def finish(request):
    logger.info('Finish note with request ' + request.body)
    note = Note.objects.get(pk=request.POST['id'])
    if note is None:
        raise Http404
    elif note.user != request.user:
        return HttpResponseForbidden()
    else:
        note.finished=True
        note.save()
        return JsonResponse(_note2Json(note))

@login_required
def reset(request):
    logger.info('Reset note with request ' + request.body)
    note = Note.objects.get(pk=request.POST['id'])
    if note is None:
        raise Http404
    elif note.user != request.user:
        return HttpResponseForbidden()
    else:
        note.finished=False
        note.save()
        return JsonResponse(_note2Json(note))

@login_required
def remove(request):
    logger.info('Remove note with request ' + request.body)
    note = Note.objects.get(pk=request.POST['id'])
    if note is None:
        raise Http404
    elif note.user != request.user:
        return HttpResponseForbidden()
    else:
        note.delete()
        return JsonResponse({})

def _note2Json(note):
    return {
        'id': note.id,
        'finished': note.finished,
        'date': note.date,
        'content': note.content
        }

