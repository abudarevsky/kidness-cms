# coding: utf-8
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
from scrollable_parts.models import ScrollableContainer
from scrollable_parts.models import ScrollablePart
from scrollable_parts.models import ScrollableNavigatorPortlet
from scrollable_parts.models import FeedbackActionPortlet

name = "Scrollables"
description = _(u"Scrollable Parts")

def install():
    """Installs the Scrollable parts application.
    """
    # Register Portlets
    register_portlet(ScrollableNavigatorPortlet, "ScrollableNavigator")
    register_portlet(FeedbackActionPortlet, u"Копка формы обратной связи")

    # Register Templates
    register_template(name = "Scrollable Overview", path="lfc/templates/scrollable_overview.html")
    register_template(name = "Carousel Overview", path="lfc/templates/jcarousel_overview.html")
    register_template(name = "Kidness Gallery", path="lfc/templates/jcarousel_gallery.html")
    register_template(name = "Video Gallery", path="lfc/templates/video_gallery.html")
    register_template(name = "Video Gallery with VK Comments", path="lfc/templates/video_gallery_vk.html")
#    register_template(name = "Scrollable Container", path="lfc/templates/scrollable_container.html")
#    register_template(name = "Scrollable Part", path="lfc/templates/scrollable_part.html")

    # Register objects
    register_content_type(ScrollableContainer, 
                          name = "Scrollable Container", 
                          templates=["Scrollable Overview","Carousel Overview"], 
                          default_template="Carousel Overview", 
                          global_addable=False)
    
    register_content_type(ScrollablePart, 
                          name = u"Scrollable Part", 
                          global_addable=False)
    
    register_content_type(Page,
        name="Page",
        sub_types=["Page"],
        templates=["Article", "Plain", "Gallery", "Overview", "Scrollable Overview","Carousel Overview", "Kidness Gallery", "Video Gallery", "Video Gallery with VK Comments"],
        default_template="Article")

    # Register Blog as a sub type of Page
    register_sub_type(ScrollableContainer, "Page")
    register_sub_type(ScrollablePart, "Scrollable Container")

def uninstall():
    """Uninstalls the ScrollNavigatorPortlet application.
    """
    # Unregister content type
    unregister_content_type("Scrollable Container")
    unregister_content_type("Scrollable Part")

    # Unregister template
    unregister_template("Scrollable Overview")
    unregister_template("Carousel Overview")
    
#    unregister_template("Scrollable Part")

    register_content_type(Page,
        name="Page",
        sub_types=["Page"],
        templates=["Article", "Plain", "Gallery", "Overview"],
        default_template="Article")

    # Unregister portlet
    unregister_portlet(ScrollableNavigatorPortlet)
    unregister_portlet(FeedbackActionPortlet)