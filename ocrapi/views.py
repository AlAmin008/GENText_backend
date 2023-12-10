from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import pytesseract
from langdetect import detect_langs
from django.http import JsonResponse
from ocrapi.models import PdfFiles,PdfDetails
from authapi.models import User
import fitz
from PIL import Image
import os
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from datetime import datetime
import string, random

#generating random number to differentiate between same named files
def generate_random(length=4):
    characters = string.digits
    value = ''.join(random.choice(characters) for _ in range(length))
    return value

#exxtracting text from image
def text_extraction(image):
    image_path = image
    img = cv2.imread(image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Configuration for Bengali language
    custom_config = r'-l eng+ben --psm 6'

    # Perform OCR
    txt = pytesseract.image_to_string(gray, config=custom_config)
    
    return txt

def pdf2image(file_path,pdf_file_instance,file_name):

    # Open the PDF file
    pdf_document = fitz.open(file_path)
    total_size = os.path.getsize(file_path)
    total_size = round (total_size/1024,2)

    total_page = 0
    # Loop through each page in the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        total_page +=1

        # Convert the page to an image
        image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))

        # Create a Pillow (PIL) image from the PyMuPDF image
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        
        user_name= "Al-Amin"
        folder_path = os.path.join(settings.BASE_DIR, f"media\{user_name}\{file_name}\pdf_Image")

        # Ensure the folder exists, create it if necessary
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Construct the complete file path with the folder
        image_filename = os.path.join(folder_path, f"page_{page_number+1}.jpg")
        pil_image.save(image_filename)

        print(image_filename)
        # print(folder_path)
        
        result = text_extraction(image_filename)

        file_instance = pdf_file_instance

        pdf_details_instance= PdfDetails(
        pdf_file_id_id= file_instance.id,
        page_number= page_number+1,
        image_location = image_filename,
        text = result
        )
        print(image_filename)
        pdf_details_instance.save()

    # Close the PDF document
    pdf_document.close()
    pdf_file_instance.total_page = total_page
    pdf_file_instance.total_size = total_size
    pdf_file_instance.upload_status = 'complete'
    pdf_file_instance.save()
    

def store_file(file_obj):
    user_name= "Al-Amin"
    garbage = generate_random()
    # Construct the complete file path with the folder
    file_name = f"{garbage}#{file_obj.name}"

    folder_path = os.path.join(settings.BASE_DIR, f"media\{user_name}\{file_name}")
    # Ensure the folder exists, create it if necessary
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path,file_name)

    with open(file_path, 'wb') as destination_file:
        for chunk in file_obj.chunks():
            destination_file.write(chunk)
                

                # adding file in database 

    user_instance = User.objects.get(id=26)
    print(file_path)  
    pdf_file_instance = PdfFiles(
    pdf_file_name= file_name,
    total_page = 0,
    total_size= 0,
    file_location= file_path,
    uploaded_by=user_instance,
    uploaded_date=datetime.now().date(),
    upload_status='pending',
    )
    #Save the instance to the database
    pdf_file_instance.save()
    return {"file_path":file_path,"file_name":file_name,"pdf_file_instance":pdf_file_instance}
# Create your views here.





class UploadFileView(APIView):

    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        file_obj = request.FILES.get('file')

        if file_obj:
            if file_obj.name.lower().endswith(".pdf"):
                obj = store_file(file_obj)
                # text extraction and saving
                pdf2image(obj["file_path"],obj["pdf_file_instance"],obj["file_name"])

                return Response({'msg': 'File successfully Stored'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Please Provide PDf files only'}, status=status.HTTP_400_BAD_REQUEST)
        else:
                return Response({'msg': 'file doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)