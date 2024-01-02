from rest_framework import serializers
from ocrapi.models import PdfFiles, PdfDetails



class UploadedFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfFiles
        fields = ['id','pdf_file_name','file_location','uploaded_date','uploaded_time', 'extraction_status','total_page','total_size','uploaded_time']

class UploadedFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfDetails
        fields = ['page_number','text','image_location']