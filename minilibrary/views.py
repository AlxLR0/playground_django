from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Book, Review, Recomendation
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ReviewForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView ,DetailView


User = get_user_model()

#para usar el class base view
class Hello(View):
    def get(self,request):
        return HttpResponse("hello")

class WelcomeView(TemplateView):
    template_name = "minilibrary/welcome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_books"] = Book.objects.count()
        return context

class BookListView(ListView):
    model = Book
    template_name = "minilibrary/book_list.html"
    paginate_by = 5
    context_object_name = "books"


class BookDetailView(DetailView):
    model = Book
    template_name = "minilibrary/book_detail.html"
    context_object_name = "book"

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "minilibrary/add_review.html"

    def form_valid(self, form):
        book_id = self.kwargs.get('pk')
        book = Book.objects.get(pk=book_id)
        form.instance.book = book
        form.instance.user = 1
        messages.success(self.request, "Gracias por la reseña")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_detail',kwargs={'pk': self.kwargs.get('pk')})
    
class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "minilibrary/add_review.html"

    def get_queryset(self):
        return Review.objects.filter(user_id=1)

    def form_valid(self, form):
        messages.success(
            self.request, "Se ha actualizo tu reseña, correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al guardara los cambios.")

    def get_success_url(self):
        review = Review.objects.get(pk=self.kwargs.get("pk"))
        book_id = review.book.id
        return reverse_lazy("book_detail", kwargs={"pk": book_id})


class ReviewDeleteView(DeleteView):
    model = Review
    template_name = "minilibrary/review_confirm_delete.html"
    success_url = reverse_lazy("book_list")

    def get_queryset(self):
        return Review.objects.filter(user_id=1)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Tu reseña fue eliminada.")
        return super().delete(request, *args, **kwargs)

   


def index(request):
    books = Book.objects.all()
    query = request.GET.get("query_search")
    date_start = request.GET.get("start")
    date_end = request.GET.get("end")

    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )

    if date_start and date_end:
        books = books.filter(publication_date__range=[
                             date_start, date_end])

    paginator = Paginator(books, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    query_string = query_params.urlencode()

    return render(request, "minilibrary/minilibrary.html", {
        "page_obj": page_obj,
        "query": query,
        "query_string": query_string
    })


#@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()

            would_recommend = form.cleaned_data.get('would_recommend')
            if would_recommend:
                # Guardar la recomendación real en la base de datos
                Recomendation.objects.get_or_create(
                    user=request.user,
                    book=book,
                    defaults={'note': 'Recomendado vía formulario de reseña'}
                )
                messages.success(
                    request, "Gracias por la reseña y tu recomendación de nuestros libros")
            else:
                messages.success(request, "Gracias por la reseña")
            return redirect("minilibrary")
        else:
            messages.error(
                request, "Corrige los errores del formulario", "danger")

    return render(request, "minilibrary/add_review.html", {
        "form": form,
        "book": book
    })