from django.views.generic import TemplateView
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
from django.views.generic import View


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