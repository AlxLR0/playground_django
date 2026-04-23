from django.contrib import admin
from .models import Author, Book, Genre, BookDetail, Review, Loan, Recomendation

# Register your models here.

admin.site.site_header = 'Administrador de la Biblioteca' #esto cambia el titulo que aparece en el django admin
admin.site.site_title = 'Panel de control de la Biblioteca'#esto cambia el titulo que aparece en el titulo de la pestaña del navegador
admin.site.index_title = 'Bienvenido al panel de control de la Biblioteca'#esto cambia el titulo que aparece en el indice


@admin.action(description="marcar prestamos como devueltos")
def mark_as_returned(modeladmin, request, queryset): #esta funcion de encarga de tomar todos los datos que se hayan seleccionado y aplicando la funcion de marcar como devueltos
    queryset.update(is_returned=True)

#personalizar campos para el django admin

#este reviewinline permite agregar una reseña al libro desde la misma interface de libro 
class ReviewInline(admin.TabularInline):
    model = Review # aqui se manda a llamar al modelo review
    extra = 1 #sirve para mostrar un cuadro en blanco mas extra de los que ya hay

class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False #evita que se borre el detalle del libro
    verbose_name_plural = 'Detalle del libro'#esto sirve para ponerle un titulo al cuadro
    
    

class BookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, BookDetailInline]#aqui se ponen los cuadros que permiten agregar informacion relacionada con el libro
    list_display = ('title', 'author', 'pages','publication_date')#columnas que se muestran en la lista
    search_fields = ('title', 'author__name', 'isbn', 'genres__name')#poner un buscador, usar __ para buscar en campos relacionados
    list_filter = ('author', 'genres', 'publication_date')#poner filtros para ordenar la lista 
    date_hierarchy = 'publication_date'#sirve para poner un buscador por fechas



class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'loan_date', 'is_returned')
    actions = [mark_as_returned] #action lo que hace es tomar los datos seleccionados y aplicar la funcion de marcar como devueltos



admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Recomendation)
