from django import template

register = template.Library()

@register.filter
def get_val(lst, index):
    if index > 0 and index < len(lst):
        return lst[index-1].sender
    return None

@register.filter
def get_sender_date(message_list, index):
    if index > 0 and index < len(message_list):
        return message_list[index - 1].created_at.date()
    return None