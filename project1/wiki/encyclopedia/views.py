from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
import markdown2

from . import util


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {"entries": entries})


def entry(request, title):
    try:
        entry = format_html(markdown2.markdown(util.get_entry(title)))
    except:
        entry = ""
    entries = util.list_entries()

    context = {
        "title": title,
        "entry": entry,
        "entries": entries
    }

    if not title in entries:
        return render(request, "encyclopedia/error.html", context)

    return render(request, "encyclopedia/entry.html", context)


def search(request):
    title = request.GET.get('q')
    try:
        entry = format_html(markdown2.markdown(util.get_entry(title)))
    except:
        entry = ""
    entries = util.list_entries()
    lowerTitle = title.lower()
    lowerEntries = []
    for item in entries:
        lowerEntries.append(item.lower())

    context = {
        "title": title, 
        "entry": entry, 
        "entries": entries
    }

    if not lowerTitle in lowerEntries:
        return render(request, "encyclopedia/error.html", context)

    return render(request, "encyclopedia/search.html", context)


def create():
    return render(request, 'encyclopedia/create.html')