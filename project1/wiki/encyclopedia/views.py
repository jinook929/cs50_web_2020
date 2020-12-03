from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
import markdown2
import random

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

    print(entry)

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


def create(request):
    if request.POST:
        title = request.POST['title']
        if title in util.list_entries():
            return render(request, 'encyclopedia/exist.html')
        save_path = '../wiki/entries/'
        fname = request.POST['title'] + ".md"
        save_file = save_path + fname
        default_storage.save(f"{save_file}", ContentFile((f"# {title}\n\n{request.POST['content']}")))
        
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

        return render(request, "encyclopedia/entry.html", context)

    return render(request, 'encyclopedia/create.html')

def edit(request):
    if request.POST:
        title = request.POST['title']
        content = f"# {title}\n\n{request.POST['content']}"
        filename = f"entries/{title}.md"
        default_storage.delete(filename)
        util.save_entry(title, content)
        entry = format_html(markdown2.markdown(util.get_entry(title)))  
        entries = util.list_entries()
        return render(request, 'encyclopedia/entry.html', { "title": title, "entry": entry, "entries": entries })
    title = request.GET.get('entry') 
    content = ""
    print(f"entries/{title}.md")
    f = str(default_storage.open(f"entries/{title}.md"))
    with open(f) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            if cnt > 2:
                content += line.strip()
            line = fp.readline()
            cnt += 1

    return render(request, "encyclopedia/edit.html", { "title": title, "content": content })

def rand(request):
    entries = util.list_entries()
    title = random.choice(entries)
    entry = format_html(markdown2.markdown(util.get_entry(title)))
    return render(request, 'encyclopedia/entry.html', { "title": title, "entry": entry, "entries": entries })