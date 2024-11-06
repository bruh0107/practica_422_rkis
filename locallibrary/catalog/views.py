from re import search

from django.http import Http404
from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Book, BookInstance, Author, Genre, Language

all_books = Book.objects.all()
wild_books = Book.objects.filter(title__contains='wild')
number_wild_books = Book.objects.filter(title__contains='wild').count()
books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    num_genres = Genre.objects.count()
    num_books_with_word = Book.objects.filter(title__icontains='cat').count()

    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,
            'num_books_with_word': num_books_with_word
        }
    )

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    template_name = 'books/my_arbitrary_template_name_list.html'

    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5]

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_sata'] = 'This is just some data'


def book_detail_view(request, pk):
    try:
        book_id = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    return render(
        request,
        'catalog/book_detail.html',
        context={'book':book_id,}
    )

class BookDetailView(generic.DetailView):
    model = Book