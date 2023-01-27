from django.http import HttpResponse
from django.template import loader

from .models import Item, Menu


def index(request):
    items_list = Item.objects.all()
    template = loader.get_template('menutree/menu.html')
    context = {
        'items_list': items_list,
    }
    return HttpResponse(template.render(context, request))
