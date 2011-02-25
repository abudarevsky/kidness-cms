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

name = "Scrollables"
description = _(u"Scrollable Parts")

def install():
    """Installs the Scrollable parts application.
    """
    # Register Portlets
    register_portlet(ScrollableNavigatorPortlet, "ScrollableNavigator")

    # Register Templates
    register_template(name = "Scrollable Overview", path="lfc/templates/scrollable_overview.html")
#    register_template(name = "Scrollable Container", path="lfc/templates/scrollable_container.html")
#    register_template(name = "Scrollable Part", path="lfc/templates/scrollable_part.html")

    # Register objects
    register_content_type(ScrollableContainer, 
                          name = "Scrollable Container", 
                          templates=["Scrollable Overview"], 
                          default_template="Scrollable Overview", 
                          global_addable=False)
    
    register_content_type(ScrollablePart, 
                          name = u"Scrollable Part", 
                          global_addable=False)
    
    register_content_type(Page,
        name="Page",
        sub_types=["Page"],
        templates=["Article", "Plain", "Gallery", "Overview", "Scrollable Overview"],
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
#    unregister_template("Scrollable Part")

    register_content_type(Page,
        name="Page",
        sub_types=["Page"],
        templates=["Article", "Plain", "Gallery", "Overview"],
        default_template="Article")

    # Unregister portlet
    unregister_portlet(ScrollableNavigatorPortlet)