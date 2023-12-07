from django.urls import path
from ocrapi.views import  UploadFileView

urlpatterns = [
    path('img2pdf/',UploadFileView.as_view(),name='text_extraction')
]
