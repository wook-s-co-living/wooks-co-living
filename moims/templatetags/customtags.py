from django import template
from ..forms import CommentForm

register = template.Library()

def get_comment_update_form(comment):
    comment_update_form = CommentForm(instance=comment)
    return comment_update_form

register.filter('get_comment_update_form', get_comment_update_form)