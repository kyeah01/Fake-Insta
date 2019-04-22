from django import template

register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content
    hashtags = post.hashtags.all()
    for hashtag in sorted(hashtags, key=lambda x : -len(x.content)):
        content = content.replace(hashtag.content, f'<a href="/posts/hashtag/{ hashtag.pk }/">{ hashtag.content }</a>', 1)
    return content