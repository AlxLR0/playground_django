from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse


# Create your views here.

days_quotes = {
    'monday': 'El éxito es la suma de pequeños esfuerzos repetidos día tras día',
    'tuesday': 'No cuentes los días, haz que los días cuenten',
    'wednesday': 'La disciplina es el puente entre metas y logros',
    'thursday': 'Tu actitud, no tu aptitud, determinará tu altitud',
    'friday': 'La felicidad no es algo hecho, viene de tus propias acciones',
    'saturday': 'Disfruta de las pequeñas cosas, un día mirarás atrás y verás que eran grandes',
    'sunday': 'Cree que puedes y casi lo habrás logrado',

}

def index(request):
    days = list(days_quotes.keys())  # Use the dictionary, not the function
    return render(request, "quotes/quotes.html", {
        "days": days
    })

def monday(request):
    return HttpResponse("Hello monday")

def tuesday(request):
    return HttpResponse("Hello tuesday")

def days_week(request, day): # esta funcion lo que hace es recibir un parametro day y devolver una frase dependiendo del dia
    try:# intenta obtener el valor de la clave day en el diccionario days_quotes
        quote_text = days_quotes[day] # aqui quote_text es igual a days_quotes donde [day] es la clave que se recibe como parametro y se busca en el diccionario days_quotes
        return HttpResponse(quote_text) # devuelve la frase 
    except Exception:
        return render(request, "404.html") # si no existe el dia, devuelve un error 404
        # raise Http404() esto es para mandar el error 404 con todo y status 404 en consola pero esto solo se usa sin el modo debug (o que se necesita estar en producion)

