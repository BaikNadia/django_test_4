from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect
from .services import BookService
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Author, Book
from .forms import AuthorForm, BookForm


class AuthorListView(ListView):
    model = Author
    template_name = 'library/authors_list.html'
    context_object_name = 'authors'


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:authors_list')

class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:authors_list')


class ReviewBookView(LoginRequiredMixin, View):
    def post(self, request, pk):  # ✅ Изменили book_id → pk
        book = get_object_or_404(Book, pk=pk)  # или id=pk

        if not request.user.has_perm('library.can_review_book'):
            return HttpResponseForbidden("У вас нет прав для рецензирования книги.")

        review_text = request.POST.get('review', '').strip()
        if review_text:
            book.review = review_text
            book.save()

        return redirect('library:book_detail', pk=book.pk)



class RecommendBookView(LoginRequiredMixin, View):
    def post(self, request, pk):  # ✅ Изменили book_id → pk
        book = get_object_or_404(Book, pk=pk)

        if not request.user.has_perm('library.can_recommend_book'):
            return HttpResponseForbidden("У вас нет прав для рекомендации книги.")

        book.recommended = True
        book.save()

        return redirect('library:book_detail', pk=book.pk)


class BooksListView(ListView):
    model = Book
    template_name = 'library/books_list.html'
    context_object_name = 'books'

# Измените BooksListView, чтобы отображались только книги, опубликованные после 2000 года

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(publication_date__year__gt=1800)

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('library:books_list')

class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'

# Добавьте метод, который будет подсчитывать количество книг данного автора,
# и передайте это значение в контекст шаблона

    def get_context_data(self, **kwargs):
        # Получаем стандартный контекст данных из родительского класса
        context = super().get_context_data(**kwargs)
        # Получаем ID книги из объекта
        book_id = self.object.id
        # Добавляем в контекст средний рейтинг и статус популярности книги
        context['average_rating'] = BookService.calculate_average_rating(book_id)
        context['is_popular'] = BookService.is_popular(book_id)
        return context


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'publication_date', 'author']
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('library:books_list')


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('library:books_list')

    # Указываем, какое право нужно
    permission_required = 'library.delete_book'

    # Опционально: что делать, если нет прав
    def handle_no_permission(self):
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(self.request.get_full_path(), self.get_login_url())
