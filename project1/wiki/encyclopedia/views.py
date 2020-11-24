from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
import markdown2

from . import util


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def error(request):
    return render(request, "encyclopedia/error.html")

def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

    return render(request, "encyclopedia/entry.html", {
        "entry": format_html(markdown2.markdown(entry))
    })
