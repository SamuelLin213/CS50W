from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

tasks = [
    "foo",
    "bar",
    "baz"
]

# Create your views here.
def index(request):
    return render(request, "tasks/index.html", { # calls index.html, with tasks passed in
        "tasks": tasks
    })

@ensure_csrf_cookie
def add(request):
    return render(request, "tasks/add.html")
