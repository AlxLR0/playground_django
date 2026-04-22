from django.contrib import admin
from .models import Author, Book, Genre, BookDetail, Review, Loan, Recomendation

# Register your models here.

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
    search_fields = ('title', 'author__name')#poner un buscador, usar __ para buscar en campos relacionados
    list_filter = ('author', 'genres', 'publication_date')#poner filtros para ordenar la lista 
    date_hierarchy = 'publication_date'#sirve para poner un buscador por fechas
    


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Loan)
admin.site.register(Recomendation)
