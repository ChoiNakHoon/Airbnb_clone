from django import template

# Templatetags를 이용해서 html 안에서 다양한 연산 할 수 있는 커스텀 테그.

register = template.Library()


@register.filter
def sexy_capitals(value):
    print(value)
    return value.capitalize()
