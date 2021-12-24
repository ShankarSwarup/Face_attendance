from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from django.conf import settings
import urllib.request
import os
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from attendance.FaceRec import FaceCamera

# Create your views here.
def index(request):
    return render(request,'templates/index.html')

def photo(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        try:
            name = request.POST['texts']
        except MultiValueDictKeyError:
            name = False
        y=os.path.join(settings.BASE_DIR,'media/')
        dir_list = os.listdir(y)
        fs= FileSystemStorage()
        name = name+".jpg"
        if name not in dir_list:
            fs.save(name,uploaded_file)
        x=os.path.join(settings.BASE_DIR,'media/',uploaded_file.name)
    return render(request,'templates/index.html')

def face(cam):
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def attendance(request):
    return StreamingHttpResponse(face(FaceCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')