from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from datetime import datetime
from .models import Item


"""def home(request):
    # Simple translatable string
    greeting = _("Hello, world!")

    # Plural example
    items = 2
    plural_text = ngettext(
        "One item available.", "%(count)s items available.", items) % {"count": items}

    # Localized date
    from django.utils import formats

    localized_date = formats.date_format(datetime.now(), "SHORT_DATE_FORMAT")

    context = {
        "greeting": greeting,
        "plural_text": plural_text,
        "localized_date": localized_date,
    }
    return render(request, "home.html", context)"""


def home(request):
    items = Item.objects.all()  # Fetch all items from the database
    context = {'items': items}  # Pass the items to the template context
    return render(request, "home.html", context)