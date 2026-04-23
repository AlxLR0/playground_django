from django.shortcuts import render
from django.http import HttpResponseServerError
# Create your views here.
def index(request):
    try:
        return render(request, 'minilibrary/minilibrary.html')
    
    except Exception:
        return HttpResponseServerError("Error al cargar los libros")