from django.urls import path
from ocrapi.views import  UploadFileView, UploadSimilarNamedFileView

urlpatterns = [
    path('img2pdf/<uid>/',UploadFileView.as_view(),name='text_extraction'),
    path('img2pdf/force/<uid>',UploadSimilarNamedFileView.as_view(),name='text_extraction')
]
