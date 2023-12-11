from django.urls import path
from fileapi.views import UploadedFilesView, UploadedFileDetailView, RecentUploadedFilesView, DashBoardView

urlpatterns = [
    path('info/<int:uid>/', UploadedFilesView.as_view(),name='uploaded-files'),
    path('detail/<int:file_id>/', UploadedFileDetailView.as_view(),name='file-detail'),
    path('recent/<int:uid>/',RecentUploadedFilesView.as_view(),name='recent-files'),
    path('dashboard/<int:uid>/',DashBoardView.as_view(),name='dash-board')
]