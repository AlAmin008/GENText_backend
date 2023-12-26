from django.db import models
from authapi.models import User

     
class PdfFiles(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('complete', 'Complete'),
        ('incomplete', 'Incomplete'),
    ]

    id = models.AutoField(primary_key=True)
    pdf_file_name = models.CharField(max_length=255)
    total_page = models.IntegerField(null = True)
    total_size = models.FloatField(null=True)
    file_location = models.CharField(max_length=300,null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_date = models.DateField(auto_now_add=True)
    upload_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    meta_data = models.TextField( null=True)
    remarks = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True)
    modified_by = models.IntegerField(null = True)

    def __str__(self):
        return f'PdfFile {self.id} - {self.pdf_file_name}'
    

class PdfDetails(models.Model):
    id = models.AutoField(primary_key=True)
    page_number = models.IntegerField()
    image_location = models.CharField(max_length=300, null=True)
    text = models.TextField()
    pdf_file_id = models.ForeignKey(PdfFiles, on_delete=models.CASCADE)
    meta_data = models.TextField(null=True)
    remarks = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True)
    modified_by = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.pdf_file_id.pdf_file_name} - Page {self.page_number}'

        
        
   