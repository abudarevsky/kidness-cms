# python imports
import datetime

# django imports
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

# tagging imports
from tagging.models import TaggedItem
from tagging.utils import get_tag

# lfc imports
from lfc.utils import traverse_object

# lfc_blog imports
from lfc_news.models import News
from lfc_news.models import NewsEntry

def archive(request, slug, month, year, template_name="lfc_news/archive.html"):
    """Display news entries for given month, year and language.
    """
    news = request.META.get("lfc_context")

    entries = []
    for entry in news.get_children(publication_date__month=month):
        if entry.has_permission(request.user, "view"):
            entries.append(entry)

    return render_to_response(template_name, RequestContext(request, {
        "blog" : news,
        "month" : _(datetime.date(int(year), int(month), 1).strftime('%B')),
        "year" : year,
        "entries" : entries,
        "lfc_context" : news,
    }))

def lfc_tagged_object_list(request, slug, tag, language=None, template_name="lfc_news/tag.html"):
    """Displays news entries for the given tag.
    """
    if tag is None:
        raise AttributeError(_('tagged_object_list must be called with a tag.'))

    tag_instance = get_tag(tag)

    if tag_instance is None:
        raise Http404(_('No Tag found matching "%s".') % tag)

    news = request.META.get("lfc_context")

    queryset = NewsEntry.objects.filter(parent=news)

    entries = []
    for entry in TaggedItem.objects.get_by_model(queryset, tag_instance):
        if entry.has_permission(request.user, "view"):
            entries.append(entry)

    return render_to_response(template_name, RequestContext(request, {
        "slug"    : slug,
        "blog"    : news,
        "entries" : entries,
        "tag"     : tag,
        "lfc_context" : news,
    }));