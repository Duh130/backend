from django.http import HttpResponse
from django.views import generic

class PosView(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('hello world')
