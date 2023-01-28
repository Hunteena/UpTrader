from django.http import HttpResponse
from django.template import loader


def menu(request):
    template = loader.get_template('menutree/menu.html')
    context = {}
    return HttpResponse(template.render(context, request))
