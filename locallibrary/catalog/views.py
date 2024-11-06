from django.shortcuts import render

# Create your views here.
from .models import Book, BookInstance, Author

all_books = Book.objects.all()
wild_books = Book.objects.filter(title__contains='wild')
number_wild_books = Book.objects.filter(title__contains='wild').count()
books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()

    return render(
        request,
        'main/index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors
        }
    )