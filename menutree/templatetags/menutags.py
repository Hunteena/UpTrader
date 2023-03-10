from django import template
from django.urls import reverse, NoReverseMatch

from menutree.models import Item

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
    active_path = context['request'].path
    ancestors_ids = []
    menu_id = None

    item_fields = ['name', 'parent', 'url', 'path']
    items = Item.objects.select_related('children').values(
        'id', *item_fields, 'children'
    )

    # Создадим словарь, где ключом является id, а значением - словарь полей,
    # в том числе соберём все дочерние пункты меню в один список,
    # а также определим список предков и обычный URL для named URL
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
        # По URL страницы определим активный пункт меню, его url и предков
        if item['url']:
            try:
                # Проверяем, является ли значение поля named URL
                items_url = reverse(item['url'])
            except NoReverseMatch:
                # Считаем, что поле содержит обычный URL
                items_url = item['url']
            items_dict[item_id]['url'] = items_url
            if items_url == active_path:
                ancestors_ids = list(map(int, item['path'].split()[1:]))
        else:
            items_url = ''
        items_dict[item_id]['url'] = items_url

        # Определим id нужного меню (верхнеуровнего объекта)
        if item['parent'] is None and item['name'] == menu_name:
            menu_id = item['id']

    if not menu_id:
        return {'error_message': f"No such menu '{menu_name}'"}

    iterator = {item_id: items_dict[item_id]
                for item_id in items_dict
                if items_dict[item_id]['parent']
                and items_dict[item_id]['parent'] == menu_id}

    return {
        "iterator": iterator,
        'items': items_dict,
        'ancestors_ids': ancestors_ids
    }
