from django.urls import path
from ocrapi.views import  UploadFileView, UploadSimilarNamedFileView

urlpatterns = [
    path('pdf2text/<uid>/',UploadFileView.as_view(),name='text_extraction'),
    path('pdf2text/force/<uid>',UploadSimilarNamedFileView.as_view(),name='text_extraction')
]
