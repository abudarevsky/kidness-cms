from django import forms
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from lfc.models import Page

# tagging imports
import tagging.models
from tagging.forms import TagField

# portlets imports
from portlets.models import Portlet

# lfc imports
from lfc.fields.autocomplete import AutoCompleteTagInput
from lfc.models import BaseContent
import lfc.utils
from tagging.models import Tag
from kidness.forms import KidnessContactForm

class ScrollableContainer(BaseContent):
    """A simple ScrollableContainer for LFC.
    """
    items_per_page = models.SmallIntegerField(default=3)
        
    class Meta:
        verbose_name=_(u'Scrollable Container')
        verbose_name_plural=_(u'Scrollable Containers')

    def get_children_pages(self):
        arr = []
        subarr = None
        for child in self.get_children():
            print child, len(arr), self.items_per_page
            if not subarr or len(subarr)>= self.items_per_page:
                subarr = []
                arr.append(subarr)
            subarr.append(child)
            print subarr
        return arr
             
    @property
    def has_more(self):
        return self.items_per_page < len(self.get_children())
    
    @property
    def get_number_of_items(self):
        return len(self.get_children())
    @property
    def get_items_enum(self):
        enum = [(n+1, ch) for n, ch in enumerate(self.get_children())]
        return enum
    
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
        fields = ("title", "display_title", "items_per_page")

class ScrollablePart(BaseContent):
    """An entry of an ScrollablePart
    """
    short_text = models.TextField(_(u"Short Text"), null=True, blank=True)
    text = models.TextField(_(u"Text"), blank=True)
    
    
    class Meta:
        verbose_name=_(u'Scrollable Part')
        verbose_name_plural=_(u'Scrollable Parts')
    
    def get_searchable_text(self):
        searchable_text = super(ScrollablePart, self).get_searchable_text()
        return searchable_text + " " + self.text

    def get_program_group_url(self):
        url = self.get_absolute_url();
        return url[:url.rfind('/')]
    def get_tags_as_list(self):
        return Tag.objects.get_for_object(self).all()

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
        fields = ("title", "display_title", "slug", "short_text", "text", "tags")

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
            "entries" : obj.get_children(),
            "form": KidnessContactForm(request=request)
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
        
class FeedbackActionPortlet(Portlet):
    """A portlet, which displays feedback action.
    """
    def __unicode__(self):
        return "%s" % self.id

    def render(self, context):
        """Renders the portlet as html.
        """
        
        obj = context.get("lfc_context")
        request = context.get("request")
            
        # CACHE
        cache_key = "%s-portlet-feedbackaction-%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, request.user.id)
        result = cache.get(cache_key)
        if result:
            return result

        result = render_to_string("scrollable_parts/feedback_action_form_portlet.html", {
            "form": KidnessContactForm(request=request)
        })

        cache.set(cache_key, result)
        return result

    def form(self, **kwargs):
        """
        """
        return FeedbackActionPortletForm(instance=self, **kwargs)

class FeedbackActionPortletForm(forms.ModelForm):
    """Form for the NewsPortlet.
    """
    class Meta:
        model = FeedbackActionPortlet        