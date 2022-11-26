from django.shortcuts import render, redirect
from django import forms
import markdown
import re
import random

from . import util
from . import forms


def index(request):

    if request.method == "POST":
        data = request.POST
        title = data['q']
        all_entries = [item.lower() for item in util.list_entries()]

        if title.lower() in all_entries:
            return redirect('entries', title = title)

        relevant_entries = []
        for item in all_entries:
            if re.search('[a-z]*[0-9]*' + title + '[a-z]*[0-9]*', item, re.IGNORECASE):
                relevant_entries.append(item)
        context = {'title': title, 'relevant_entries': relevant_entries}
        return render(request, "encyclopedia/search.html", context)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, title):
    entry = util.get_entry(title)
    if entry:
        entry = markdown.markdown(entry)
    context = {'title': title, 'entry': entry}
    return render(request, "encyclopedia/entries.html", context)

def random_page(request):
    all_entries = util.list_entries()    
    title = all_entries[random.randint(0, len(all_entries) - 1)]
    return redirect('entries', title=title)

def create(request):
    if request.method == "POST":
        form = forms.createForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            if util.get_entry(title):
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": "Entry already exists"
                })
            util.save_entry(title, body)
            return redirect('entries', title=title)

    context = {'form': forms.createForm()}
    return render(request, "encyclopedia/create.html", context)

def edit(request, title):
    if request.method == "POST":
        form = forms.createForm(request.POST) # when editing, the form is the same as the create form
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            util.save_entry(title, body)
            return redirect('entries', title=title)

    entry = util.get_entry(title)
    form = forms.createForm(initial={'title': title, 'body': entry}) # populate the form with the entry's title and body
    return render(request, "encyclopedia/edit.html", {'form': form})

