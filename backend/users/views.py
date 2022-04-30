from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser import utils
from djoser.views import TokenDestroyView
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from foodgram.pagination import LimitPageNumberPaginator
from .models import Follow, User
from .serializers import FollowSerializer
