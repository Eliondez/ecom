from django.http import HttpResponse
from django.shortcuts import render

from user.models import User
from .utils import create_fake_tasks


def index_view(request):

    return render(request, 'main/index.html')
