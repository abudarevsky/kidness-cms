# -*- encoding: utf-8 -*-
# django imports
from django.conf import settings
from django.core.cache import cache
from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _

# portlets imports
import portlets.utils
from portlets.models import Slot
from django.template.loader import render_to_string
from kidness.forms import KidnessContactForm

register = Library()

class SlotsInformationNode(Node):
    """
    """
    def render(self, context):
        obj = context.get("lfc_context")
        request = context.get("request")

        if obj:
            cache_key = "%s-slots-information-%s-%s-%s" % \
                (settings.CACHE_MIDDLEWARE_KEY_PREFIX, obj.content_type, obj.id, request.user.id)
        else:
            cache_key = "%s-slots-information-portal-%s" % \
                (settings.CACHE_MIDDLEWARE_KEY_PREFIX, request.user.id)

        info = cache.get(cache_key)
        if info:
            context["content_class"] = info["content_class"]
            context["SlotLeft"] = info["SlotLeft"]
            context["SlotRight"] = info["SlotRight"]
            return ''

        if obj:
            obj = obj.get_content_object()

        for slot in Slot.objects.all():
            context["Slot%s" % slot.name] = portlets.utils.has_portlets(slot, obj)

        if context["SlotLeft"] and context["SlotRight"]:
            content_class = "span-13 append-1"
        elif context["SlotLeft"]:
            content_class = "span-18 last"
        elif context["SlotRight"]:
            content_class = "span-18 append-1"
        else:
            content_class = "span-24 last"

        cache.set(cache_key, {
            "content_class" : content_class,
            "SlotLeft" : context["SlotLeft"],
            "SlotRight" : context["SlotRight"],
        })

        context["content_class"] = content_class
        return ''

def do_slots_information(parser, token):
    """Calculates some context variables based on displayed slots.
    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits != 1:
        raise TemplateSyntaxError(_('%s tag needs no argument') % bits[0])

    return SlotsInformationNode()

@register.filter
def gt(a, b):
    return a > b

@register.filter
def month_as_text(num):
    months = {
              1: u"января",
              2: u"февраля",
              3: u"марта",
              4: u"апреля",
              5: u"мая",
              6: u"июня",
              7: u"июля",
              8: u"августа",
              9: u"сентября",
              10: u"октября",
              11: u"ноября",
              12: u"декабря",
              }
    return months[int(num)]

#register.tag('gt', gt)

register.tag('slots_information', do_slots_information)

class KidnessContactFormNode(Node):
   
    def render(self, context):
        request = context.get('request')
        
        formstr = render_to_string("scrollable_parts/scrollable_contactform_new.html",
                                   {"form" : KidnessContactForm(request=request)}, context)
        return formstr
def get_kidness_contactform_new(parser, token):
    return KidnessContactFormNode()
        
register.tag('kidness_contactform_new', get_kidness_contactform_new)  