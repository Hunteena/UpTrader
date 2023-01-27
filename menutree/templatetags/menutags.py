from django import template

from menutree.models import Item, Menu

register = template.Library()


@register.inclusion_tag('menutree/sublist.html', takes_context=True)
def draw_children(context, item_id, children):
    items_dict = context['items']
    ancestors_ids = context['ancestors_ids']
    if item_id in ancestors_ids and any(children):
        iterator = {item_id: items_dict[item_id] for item_id in children}
    else:
        iterator = {}
    return {
        'iterator': iterator,
        'items': items_dict,
        'ancestors_ids': ancestors_ids
    }


@register.inclusion_tag('menutree/sublist.html', takes_context=True)
def draw_menu(context, menu_name):
    menu = Menu.objects.filter(name=menu_name).first()
    if not menu:
        return {'no_menu_error': 'No such menu'}

    active_path = context['request'].path
    ancestors_ids = []

    item_fields = ['name', 'path', 'url']
    items = Item.objects.filter(
        path__startswith=f"{menu.id} "
    ).select_related(
        'children'
    ).values(
        'id', *item_fields, 'children'
    )
    items_dict = dict()
    for item in items:
        item_id = item['id']
        child = item['children']
        if item_id in items_dict:
            items_dict[item_id]['children'].append(child)
        else:
            items_dict[item_id] = {'children': [child]}
            for field in item_fields:
                items_dict[item_id][field] = item[field]
        if item['url'] == active_path:
            ancestors_ids = list(map(int, item['path'].split(' ')[1:]))

    iterator = {item_id: items_dict[item_id]
                for item_id in items_dict
                if items_dict[item_id]['parent'] is None}

    return {
        "iterator": iterator,
        'items': items_dict,
        'ancestors_ids': ancestors_ids
    }
