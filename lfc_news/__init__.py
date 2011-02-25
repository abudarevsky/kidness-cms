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

# lfc_news imports
from lfc_news.models import News
from lfc_news.models import NewsPortlet
from lfc_news.models import NewsEntry

name = "News"
description = _(u"News feed")

def install():
    """Installs the blog application.
    """
    # Register Portlets
    register_portlet(NewsPortlet, "News")

    # Register Templates
    register_template(name = "News", path="lfc/templates/news.html")
    register_template(name = "News Entry", path="lfc/templates/news_entry.html")

    # Register objects
    register_content_type(NewsEntry, name = "News Entry", templates=["News Entry"], default_template="News Entry", global_addable=False)
    register_content_type(News, name = "News", sub_types = ["NewsEntry"], templates=["News"], default_template="News")

    # Register Blog as a sub type of Page
    register_sub_type(News, "Page")

def uninstall():
    """Uninstalls the blog application.
    """
    # Unregister content type
    unregister_content_type("News")
    unregister_content_type("News Entry")

    # Unregister template
    unregister_template("News")
    unregister_template("News Entry")

    # Unregister portlet
    unregister_portlet(NewsPortlet)