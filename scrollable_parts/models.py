from django import forms
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from lfc.models import Page

import tagging.models

# tagging imports
import tagging.models
from tagging.forms import TagField

# portlets imports
from portlets.models import Portlet

# lfc imports
from lfc.fields.autocomplete import AutoCompleteTagInput
from lfc.models import BaseContent
import lfc.utils

class ScrollableContainer(BaseContent):
    """A simple ScrollableContainer for LFC.
    """
    items_per_page = models.SmallIntegerField(default=3)
        
    class Meta:
        verbose_name=_(u'Scrollable Container')
        verbose_name_plural=_(u'Scrollable Containers')

    def get_children_pages(self):
        print 'get_children_pages', self.get_children()
        arr = []
        subarr = None
        for child in self.get_children():
            print child, len(arr), self.items_per_page
            if not subarr or len(subarr)>= self.items_per_page:
                print 'New subarr'
                subarr = []
                arr.append(subarr)
                print 'subarr added', arr
            print 'Adding child', child    
            subarr.append(child)
            print subarr
        print 'Arr', arr    
        return arr         

    def form(self, **kwargs):
        """Returns the add/edit form of the News
        """
        return ScrollableContainerForm(**kwargs)

from lfc.manage.forms import CoreDataForm

class ScrollableContainerForm(CoreDataForm):
    """The add/edit form of the News content object
    """
    class Meta:
        model = ScrollableContainer
        fields = ("title", "display_title", "description", "items_per_page")

class ScrollablePart(BaseContent):
    """An entry of an News
    """
    text = models.TextField(_(u"Text"), blank=True)
    
    class Meta:
        verbose_name=_(u'Scrollable Part')
        verbose_name_plural=_(u'Scrollable Parts')
    
    def get_searchable_text(self):
        searchable_text = super(ScrollablePart, self).get_searchable_text()
        return searchable_text + " " + self.text
    def get_tag_list(self):
        return tagging.models.Tag.objects.usage_for_model(
                ScrollablePart, filters = {
                    "parent" : self,
                })

    def form(self, **kwargs):
        """Returns the add/edit form of the NewsEntry
        """
        return ScrollablePartForm(**kwargs)

class ScrollablePartForm(forms.ModelForm):
    """The add/edit form of the News content object
    """
    tags = TagField(widget=AutoCompleteTagInput(), required=False)
    class Meta:
        model = ScrollablePart
        fields = ("title", "display_title", "slug", "description", "text", "tags")

class ScrollableNavigatorPortlet(Portlet):
    """A portlet, which displays recent entries, archive and tag cloud.
    """
    limit = models.IntegerField(default=5)

    def __unicode__(self):
        return "%s" % self.id

    def render(self, context):
        """Renders the portlet as html.
        """
        
        obj = context.get("lfc_context")
        request = context.get("request")
        if not isinstance(obj, ScrollableContainer):
            for child in obj.get_children():
                if isinstance(child, ScrollableContainer):
                    obj=child
                    break 
            
        # CACHE
        cache_key = "%s-portlet-scrollable-%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, request.user.id)
        result = cache.get(cache_key)
        if result:
            return result

        result = render_to_string("scrollable_parts/scrollable_navigator_portlet.html", {
            "page" : obj,
            "title" : self.title,
            "entries" : obj.get_children()
        })

        cache.set(cache_key, result)
        return result

    def form(self, **kwargs):
        """
        """
        return ScrollableNavigatorPortletForm(instance=self, **kwargs)

class ScrollableNavigatorPortletForm(forms.ModelForm):
    """Form for the NewsPortlet.
    """
    class Meta:
        model = ScrollableNavigatorPortlet