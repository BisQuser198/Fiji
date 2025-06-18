from django.test import TestCase

# Create your tests here.
import shutil

def clone_docx():
    source_path = r"C:\Users\I5\Desktop\python_work\Django 5Jun2025.docx"
    destination = r"C:\Users\I5\Desktop\python_work\Test.docx"
    shutil.copy2(source_path, destination)

# need to run this