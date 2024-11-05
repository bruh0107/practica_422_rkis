from django.shortcuts import render

# Create your views here.
from .models import Book

all_books = Book.objects.all()
wild_books = Book.objects.filter(title__contains='wild')
number_wild_books = Book.objects.filter(title__contains='wild').count()
books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')
