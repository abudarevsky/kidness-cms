# python imports
import datetime

# django imports
from django import forms
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# tagging imports
import tagging.models
from tagging.forms import TagField

# portlets imports
from portlets.models import Portlet

# lfc imports
from lfc.fields.autocomplete import AutoCompleteTagInput
from lfc.models import BaseContent
import lfc.utils

class News(BaseContent):
    """A simple News for LFC.
    """
    text = models.TextField(_(u"Text"), blank=True)
        
    class Meta:
        verbose_name=_(u'News feed')
        verbose_name_plural=_(u'News feeds')
        ordering = ["-creation_date"]

    def get_searchable_text(self):
        searchable_text = super(News, self).get_searchable_text()
        return searchable_text + " " + self.text

    def form(self, **kwargs):
        """Returns the add/edit form of the News
        """
        return NewsForm(**kwargs)

class NewsForm(forms.ModelForm):
    """The add/edit form of the News content object
    """
    class Meta:
        model = News
        fields = ("title", "display_title", "slug", "description", "text")

class NewsEntry(BaseContent):
    """An entry of an News
    """
    text = models.TextField(_(u"Text"), blank=True)
    
    class Meta:
        verbose_name=_(u'News entry')
        verbose_name_plural=_(u'News entries')
        ordering = ["-creation_date"]
    
    def get_searchable_text(self):
        searchable_text = super(NewsEntry, self).get_searchable_text()
        return searchable_text + " " + self.text

    def form(self, **kwargs):
        """Returns the add/edit form of the NewsEntry
        """
        return NewsEntryForm(**kwargs)

class NewsEntryForm(forms.ModelForm):
    """The add/edit form of the News content object
    """
    tags = TagField(widget=AutoCompleteTagInput(), required=False)
    class Meta:
        model = NewsEntry
        fields = ("title", "display_title", "slug", "description", "text", "tags")

class NewsPortlet(Portlet):
    """A portlet, which displays recent entries, archive and tag cloud.
    """
    limit = models.IntegerField(default=5)
    show_archive = models.BooleanField(_(u'Show archive'),help_text=_(u'Say Yes if you want show archived entries in the portlet'), default=True)
    show_tags = models.BooleanField(_(u'Show topics'), help_text=_(u'Say Yes if you want show topics in the portlet'), default=True)

    def __unicode__(self):
        return "%s" % self.id

    def render(self, context):
        """Renders the portlet as html.
        """
        
        obj = context.get("lfc_context")
        request = context.get("request")
        
        # CACHE
        cache_key = "%s-portlet-news-%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, request.user.id)
        result = cache.get(cache_key)
        if result:
            return result

#        from lfc_news.models import NewsEntry, News
        if not (isinstance(obj, NewsEntry) or isinstance(obj, NewsEntry)):
            obj = News.objects.all()[0]
            
        # Urgh! Ugly hack.
        if isinstance(obj, NewsEntry):
            obj = obj.parent
        
        now = datetime.datetime.now()
        entries = NewsEntry.objects.order_by('-creation_date').get_content_objects()[:self.limit]
#        entries = obj.get_children(request)[:self.limit]

        years = []
        if self.show_archive:
            for year in range(now.year, now.year-4, -1):
                months = []
                for i in range(12, 0, -1):
                    month = (now.month+i) % 12
                    if month == 0:
                        month = 12
    
                    amount = len(obj.get_children(request, publication_date__month=month, publication_date__year=year))
    
                    if amount:
                        months.append({
                            "name" : _(datetime.date(now.year, month, 1).strftime('%B')),
                            "amount" : amount,
                            "number" : month,
                        })
                if months:
                    years.append({
                        "year" : year,
                        "months" : months
                    })
        cloud = []
        if self.show_tags:            
            cloud = tagging.models.Tag.objects.cloud_for_model(
                NewsEntry, filters = {
                    "parent" : obj,
                })

        result = render_to_string("lfc_news/news_portlet.html", {
            "page" : obj,
            "title" : self.title,
            "entries" : entries,
            "years" : years,
            "year" : now.year,
            "cloud" : cloud,
        })

        cache.set(cache_key, result)
        return result

    def form(self, **kwargs):
        """
        """
        return NewsPortletForm(instance=self, **kwargs)

class NewsPortletForm(forms.ModelForm):
    """Form for the NewsPortlet.
    """
    class Meta:
        model = NewsPortlet
