# Project Setup

To setup this in your pc make sure to install those followings:

- Install and setup Django
- Django REST API (pip install djangorestframework)
- SimpleJWT (pip install djangorestframework-simplejwt)
- core headers (pip install django-cors-headers)
- mysqlclient (pip install mysqlclient)
- opencv (pip install opencv-python)
- Downlaod and install pytesseract exe (https://github.com/UB-Mannheim/tesseract/wiki)
- After installing add the path of pytesseract exe in setttings.py
  {pytesseract.pytesseract.tesseract_cmd = '{your_path}/tesseract.exe'}
- pytesseract (pip install pytesseract)
- download ben.tessdata from here (https://github.com/tesseract-ocr/tessdata) and place the downloaded file into your installed pytessearct tessdata folder
- Install PyMuPDF (pip install PyMuPDF)


#Version
 - django 4.2.4
 - mariadb 15.1
 - django REST framework 3.14.0
 - opencv 4.8.1
 - simpleJWT 5.3.1
 - mysqlclient 2.2.0
 - pytesseract 0.3.10
 - PyMuPdf 1.23.6
