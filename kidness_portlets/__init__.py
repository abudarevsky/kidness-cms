# django imports
from django.utils.translation import ugettext_lazy as _

# lfc imports
from lfc.utils.registration import register_content_type
from lfc.utils.registration import unregister_content_type
from lfc.utils.registration import register_sub_type
from lfc.utils.registration import register_template
from lfc.utils.registration import unregister_template

# portlets imports
from portlets.utils import register_portlet
from portlets.utils import unregister_portlet

from lfc.models import Page

# lfc_news imports
from kidness_portlets.models import TextBlockPortlet, SlideshowPortlet

name = "Kidness portlets"
description = _(u"Kidness Portlets")

def install():
    """Installs the Scrollable parts application.
    """
    # Register Portlets
    register_portlet(TextBlockPortlet, "TextBlock")
    register_portlet(SlideshowPortlet, "Slideshow")

def uninstall():
    unregister_portlet(TextBlockPortlet)
    unregister_portlet(SlideshowPortlet)
