# django imports
from django.template import Library, Node
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from kidness.forms import KidnessContactForm

register = Library()

class KidnessContactFormNode(Node):
   
    def render(self, context):
        request = context.get('request')
        
        formstr = render_to_string("scrollable_parts/scrollable_contactform.html",
                                   {"form" : KidnessContactForm(request=request)}, context)
        return formstr
def get_kidness_contactform(parser, token):
    return KidnessContactFormNode()
        
register.tag('kidness_contactform', get_kidness_contactform)        
