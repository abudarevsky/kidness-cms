# coding: UTF-8
import re
import random

# django imports
from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

# tagging imports
import tagging

from tagging.forms import TagField

from lfc.fields.autocomplete import AutoCompleteTagInput
from lfc.models import BaseContent

# portlets imports
from portlets.models import Portlet


class TextBlockPortlet(Portlet):
    """A portlet to display random objects. The objects can be selected by
    tags.

    **Attributes:**

    limit:
        The amount of objects which are displayed at maximum.

    tags:
        The tags an object must have to be displayed.
    """
    tags = models.CharField(blank=True, max_length=100)
    random = models.BooleanField(_(u'Random order'),default=False)
    show_more = models.BooleanField(_(u'Read more'),default=False)
    has_all_tags = models.BooleanField(_(u'Include all tags'),default=False)

    def render(self, context):
        """Renders the portlet as HTML.
        """
        items = BaseContent.objects.filter(language__in=("0", translation.get_language()))
        if self.tags:
            if self.has_all_tags:
                items = tagging.managers.ModelTaggedItemManager().with_all(self.tags, items)
            else:
                items = tagging.managers.ModelTaggedItemManager().with_any(self.tags, items)    
        items = list(items)
        if self.random:
            random.shuffle(items)
            
#        print items    
#        if self.limit:
#            items = items[:self.limit]
            
        return render_to_string("textblock_portlet.html", {
            "title" : self.title,
#            "items" : items[:self.limit],
            "items" : items[:1],
            "show_more": self.show_more
        })

    def form(self, **kwargs):
        """Returns the form of the portlet.
        """
        return TextBlockPortletForm(instance=self, **kwargs)

class TextBlockPortletForm(forms.ModelForm):
    """Add/Edit form for the random portlet.
    """
    tags = TagField(widget=AutoCompleteTagInput(), required=False)

    class Meta:
        model = TextBlockPortlet

class SlideshowPortlet(Portlet):
    tags = models.CharField(blank=True, max_length=100)
    interval = models.IntegerField(_(u'Интервал, сек'), default=4)
    random = models.BooleanField(_(u'Random order'),default=False)
    has_all_tags = models.BooleanField(_(u'Include all tags'),default=False)
    
    def render(self, context):
        """Renders the portlet as HTML.
        """
        items = BaseContent.objects.filter(language__in=("0", translation.get_language()))
        if self.tags:
            if self.has_all_tags:
                items = tagging.managers.ModelTaggedItemManager().with_all(self.tags, items)
            else:
                items = tagging.managers.ModelTaggedItemManager().with_any(self.tags, items)    
        items = list(items)
        if self.random:
            random.shuffle(items)
        return render_to_string("slideshow_portlet.html", {
            "title" : self.title,
            "items" : items,
            "rotate": len(items)>1,
            "interval": self.interval
        })

    def form(self, **kwargs):
        """Returns the form of the portlet.
        """
        return SlideshowPortletForm(instance=self, **kwargs)

class SlideshowPortletForm(forms.ModelForm):
    """Add/Edit form for the random portlet.
    """
    tags = TagField(widget=AutoCompleteTagInput(), required=False)

    class Meta:
        model = SlideshowPortlet    
