import re

from django import template
from django.urls import reverse, NoReverseMatch
import json
import pytz

utc=pytz.UTC

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''

@register.simple_tag(takes_context=True)
def convert_to_json(context, string):
    print(type(json.loads(string)))
    return json.loads(string)


@register.filter
def convert_json(value):
    return json.loads(value)


@register.filter
def handle_none(value):

    if value:
        return value
    return '-'

@register.filter
def handle_none_blank(value):
    if value:
        return value
    return ''

@register.filter
def handle_none_n_a(value):
    if value == 'na':
        return 'N/A'

    if value == 'NA':
        return 'N/A'

    if value:
        return value
    return 'N/A'

@register.filter
def format_space(value):
    try:
        text = ''.join(' ' + char if char.isupper() else char.strip() for char in value).strip()
        return text
    except:
        return value


@register.filter
def handle_rate(value):
    if value:
        rate = ' ' + '$' + str(value)
        return rate
    else:
        return 'N/A'


@register.filter
def get_class_subjects(class_obj):
    return class_obj.subjects.filter(is_active=True)

@register.filter
def get_class_subjects_videos(subject):
    return subject.videos.filter(is_active=True)






