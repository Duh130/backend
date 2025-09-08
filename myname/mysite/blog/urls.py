# blog/urls.py
from django.urls import path
from .post_view import PosView  # importa a classe que você criou

urlpatterns = [
    path('', PosView.as_view(), name='home'),  # aqui usamos .as_view() para class-based views
]