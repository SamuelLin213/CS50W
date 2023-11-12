from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import secrets

class NewCreateForm(forms.Form):
    title = forms.CharField(label='New Title')
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))
class NewEditForm(forms.Form):
    title = forms.CharField(label='New Title')
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    page = util.get_entry(name)
    if page is None:
        return render(request, "encyclopedia/error.html", {
            "title": name
        })
    return render(request, "encyclopedia/entry.html", {
        "title": name,
        "contents": markdown2.markdown(page)
    })

def search(request):
    entries = util.list_entries() # get all entries

    query = request.GET.get("q", "") # get search term
    page = util.get_entry(query) # get page of query

    if query in entries: # found query in entries list
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "contents": markdown2.markdown(page)
        })  # call entry of match

    # check if query exists as substring
    results = []
    for e in entries:
        if query.lower() in e.lower():
            results.append(e)

    return render(request, "encyclopedia/index.html", {
        "entries": results
    })

def create(request):
    if request.method == "POST":
        form = NewCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["content"]
            savePage = util.save_entry(title, markdown)
            if savePage == None:
                return render(request, "encyclopedia/duplicate.html", {
                    "title": title
                })
            else:
                return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewCreateForm()
    })

def edit(request, name):
    contents = util.get_entry(name)
    if request.method == "POST":
        form = NewEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["content"]
            util.edit_entry(title, markdown)
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "name": name,
                "contents": contents
            })

    return render(request, "encyclopedia/edit.html", {
        "form": NewEditForm(initial={'title': name, 'content': contents}),
        "name": name,
        "contents": contents
    })

def random(request):
    entries = util.list_entries()
    page = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=(page,)))
