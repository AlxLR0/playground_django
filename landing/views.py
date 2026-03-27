from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
# Create your views here.

stack=[{'id': 'python', 'name': 'python'},
       {'id': 'django', 'name': 'django'},
       {'id': 'react', 'name': 'react'},
       {'id': 'tailwind', 'name': 'tailwind'}]

def home(request):
    today = date.today()
    return render(request, 'landing/landing.html', {
        'name': 'Alex',
        'today': today,
        'age': 26,
        'fruits': ['apple', 'banana', 'cherry'],
        'stack': stack
    })

def stack_detail(request, tool):
    return HttpResponse(f'<h1>Tecnologia: {tool}</h1>')