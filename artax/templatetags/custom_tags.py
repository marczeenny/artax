from django import template
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_link(context, link, text, icon):
    if context['request'].resolver_match.view_name.endswith(link):
        nav_class = 'nav-item'
        link_class = 'nav-link'
    else:
        nav_class = 'nav-item collapsed'
        link_class = 'nav-link collapsed'

    url = context['request'].build_absolute_uri(reverse(link))

    return mark_safe(f"""<li class="{nav_class}"><a class="{link_class}" href="{url}"><i class="bi bi-{icon}"></i><span>{text}</span></a></li>""")