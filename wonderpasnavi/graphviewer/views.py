from django.shortcuts import render
from .models import Image

# Create your views here.
def image_list(request):
    images = Image.objects.all()
    return render(request, 'graphviewer/image_list.html', {'images': images})