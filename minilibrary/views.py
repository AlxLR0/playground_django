from minilibrary.models import Book
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseServerError
from django.core.paginator import Paginator

# --- VISTA PRINCIPAL (Muestra la lista de libros) ---
def index(request):
    try:
        # 1. Empezamos con todos los libros de la base de datos.
        books = Book.objects.all()

        # 2. FILTRO POR RANGO DE FECHAS
        # Intentamos obtener las fechas de inicio y fin desde la dirección (URL).
        date_start = request.GET.get('start')
        date_end = request.GET.get('end')

        if date_start and date_end:
            # Si el usuario puso fechas, filtramos los libros que se publicaron en ese periodo.
            books = books.filter(publication_date__range=[date_start, date_end])

        # 3. BUSCADOR POR TEXTO
        # Obtenemos lo que el usuario escribió en el cuadrito de búsqueda.
        query = request.GET.get('query_search')
        if query:
            # Buscamos libros cuyo título TENGA ese texto O cuyo autor TENGA ese texto.
            # 'icontains' significa que no importa si es Mayúscula o minúscula.
            books = books.filter(Q(title__icontains=query) | Q(author__name__icontains=query))

        # 4. PAGINACIÓN (Para no mostrar 1000 libros de golpe)
        # Configuramos para mostrar solo 5 libros por "hoja" o página.
        paginator = Paginator(books, 5)
        # Miramos en qué número de página está el usuario ahora mismo.
        page_number = request.GET.get('page')
        # Obtenemos los libros que corresponden a esa página específica.
        page_obj = paginator.get_page(page_number)

        # 5. PREPARAR LOS PARÁMETROS DE BÚSQUEDA
        # Esto sirve para que, al pasar a la página 2, Django recuerde qué estabas buscando.
        query_params = request.GET.copy()
        if 'page' in query_params:
            # Quitamos el parámetro 'page' de la copia para que no se amontone.
            del query_params['page']

        # 6. RESPUESTA (Enviar los datos al archivo HTML)
        return render(request, 'minilibrary/minilibrary.html', {
            'page_obj': page_obj,         # Enviamos los libros de la página actual.
            'query_params': query_params.urlencode(), # Los filtros para los botones de "Siguiente/Anterior".
            'query_search': query or ''   # El texto buscado para que no se borre del cuadro.
        })

    except Exception as e:
        # Si ocurre un error inesperado, mandamos un mensaje de error 500.
        return HttpResponseServerError(f"Ocurrió un error en el servidor: {e}")