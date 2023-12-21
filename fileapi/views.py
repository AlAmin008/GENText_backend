from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from fileapi.serializers import  UploadedFilesSerializer, UploadedFileDetailSerializer
from rest_framework.permissions import IsAuthenticated
from ocrapi.models import PdfFiles, PdfDetails
from django.db.models import Count, Case, When

def get_pdf_file_status_counts(user_id):
    return PdfFiles.objects.filter(uploaded_by_id=user_id).aggregate(
        Successful= Count(Case(When(upload_status='complete', then=1))),
        Processing= Count(Case(When(upload_status='pending', then=1))),
        Unsuccessful= Count(Case(When(upload_status='incomplete', then=1))), 
        Total = Count('upload_status')
    )

# Create your views here.
class UploadedFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,uid):
        files = PdfFiles.objects.filter(uploaded_by=uid).order_by('-id')
        serializer = UploadedFilesSerializer(files,many=True)
        if not files:
            return Response({"msg":"No File Uploaded Yet"},status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UploadedFileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,file_id):
        info = PdfDetails.objects.filter(pdf_file_id=file_id).order_by('page_number')
        serializer = UploadedFileDetailSerializer(info,many=True)
        if not info:
            return Response({"msg":"Unable to fetch data"},status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RecentUploadedFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,uid):
        files = PdfFiles.objects.filter(uploaded_by=uid).order_by('-id').values()[:5]
        serializer = UploadedFilesSerializer(files,many=True)
        if not files:
            return Response({"msg":"No File Uploaded Yet"},status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DashBoardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,uid):
        result = get_pdf_file_status_counts(uid)
        return Response({"data":result}, status=status.HTTP_200_OK)
