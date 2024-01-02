from django.urls import path
from ocrapi.views import  UploadFileView, UploadSimilarNamedFileView, Pdf2ImageView,Image2TextView

urlpatterns = [
    path('upload-pdf/<uid>/',UploadFileView.as_view(),name='upload-file'),
    path('upload-pdf/force/<uid>/',UploadSimilarNamedFileView.as_view(),name='upload-similar-file'),
    path('pdf2image/<fileid>/',Pdf2ImageView.as_view(),name='pdf-2-image'),
    path('image2text/<fileid>/',Image2TextView.as_view(),name="text-extraction")
]
