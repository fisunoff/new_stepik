from django.shortcuts import render
from .tag_manager import manager


def tags_view(request):
    tags = []
    for tag_name, tag in manager.get_tags().items():
        tags.append((tag_name, tag.description))
    return render(request, "tags/list.html", {"tags": tags})
