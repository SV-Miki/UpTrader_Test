from django import template
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

from menus.models import Menu, MenuItem

register = template.Library()


def normalize_url(p: str) -> str:
    """Приводим URL к виду с слешами в начале и конце."""
    return "/" + p.strip("/") + "/"


def expand_active_nodes(nodes, active_id):
    """Отмечаем активный узел и раскрываем всех родителей и детей первого уровня."""
    cur_id = active_id
    if cur_id in nodes:
        nodes[cur_id]["is_active"] = True

    # Идём вверх по дереву, разворачивая родителей
    while cur_id:
        node = nodes.get(cur_id)
        if not node:
            break
        node["expanded"] = True
        parent_obj = node["obj"].parent
        cur_id = parent_obj.id if parent_obj else None

    # Разворачиваем первый уровень вложенности под активным элементом
    active_node = nodes.get(active_id)
    if active_node:
        for child in active_node["children"]:
            child["expanded"] = True


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context.get("request")

    # Получаем меню по имени
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return ""

    # Получаем все элементы меню одним запросом
    items = list(
        MenuItem.objects.filter(menu=menu)
        .select_related("parent")
        .order_by("order", "id")
    )

    # Строим дерево
    nodes = {}
    children_map = {}
    for it in items:
        nodes[it.id] = {
            "obj": it,
            "children": [],
            "is_active": False,
            "expanded": False,
        }
        children_map.setdefault(it.parent_id, []).append(it.id)

    for parent_id, child_ids in children_map.items():
        if parent_id is None:
            continue
        parent_node = nodes.get(parent_id)
        if parent_node:
            parent_node["children"].extend(nodes[cid] for cid in child_ids)

    roots = [nodes[cid] for cid in children_map.get(None, [])]

    # Определяем активный элемент
    current_path = getattr(request, "path", "")
    active_node_id = None
    for it in items:
        try:
            item_url = it.get_url()
        except Exception:
            item_url = ""
        if item_url and normalize_url(item_url) == normalize_url(current_path):
            active_node_id = it.id
            break

    if active_node_id:
        expand_active_nodes(nodes, active_node_id)

    # Рендерим меню
    html = render_to_string(
        "menus/menu.html",
        {
            "menu_name": menu_name,
            "menu_title": menu.title,
            "roots": roots,
            "request": request,
        },
    )
    return mark_safe(html)
