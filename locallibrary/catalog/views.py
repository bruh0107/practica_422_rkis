from itertools import product
from re import search

from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.template.defaultfilters import title
from django.utils.translation.trans_real import catalog
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime

from .forms import RenewBookModelForm
from .models import Book, BookInstance, Author, Genre, Language

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    num_genres = Genre.objects.count()
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    user_librarian = request.user.groups.filter(name='Librarians').exists()

    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,
            'num_visits': num_visits,
            'user_librarian': user_librarian,
        }
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    template_name = 'catalog/book_list.html'

    def get_queryset(self):
        cart = self.request.session.get('cart', [])

        cart_ids = [int(book_id) for book_id in cart]

        return Book.objects.exclude(id__in=cart_ids)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

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

class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooks(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect('all-borrowed')

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={
            'renewal_date': proposed_renewal_date,
        })

    return render(request,
                  'catalog/book_renew_librarian.html',
                  {'form': form, 'bookinst': book_inst})

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = { 'date_of_death': '07/11/2024' }
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('author')
    permission_required = 'catalog.delete_author'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'


@login_required
def add_to_cart(request, pk):
    book_id = str(pk)

    cart = request.session.get('cart', [])

    if book_id not in cart:
        cart.append(book_id)

    request.session['cart'] = cart

    return redirect('books')
