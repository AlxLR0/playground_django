from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect


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
    return HttpResponse("Hello World")

def monday(request):
    return HttpResponse("Hello monday")

def tuesday(request):
    return HttpResponse("Hello tuesday")

def days_week(request, day): # esta funcion lo que hace es recibir un parametro day y devolver una frase dependiendo del dia
    try:# intenta obtener el valor de la clave day en el diccionario days_quotes
        quote_text = days_quotes[day] # aqui quote_text es igual a days_quotes donde [day] es la clave que se recibe como parametro y se busca en el diccionario days_quotes
        return HttpResponse(quote_text) # devuelve la frase 
    except Exception:
        return HttpResponseNotFound("No existe ese dia") # si no existe el dia, devuelve un error 404
