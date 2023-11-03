from django import template

register = template.Library()

# если не зарегестрировать фильтры, то django никогда не узнает, где именно их искать и фильтры потеряются
@register.filter(name='Censor')
def censor(value):
    badWords = value.split()
# Список нежелательных слов, которые нужно заменить
    STOP_LIST = [
        'более',
        'нежелательно',
        'заменяемоеслово',
        'мат'
    ]
# Преобразование слов в символы "*"
    for word in badWords:
        if word in STOP_LIST:
            value = value.replace(word,'*' * len(word))
    return value
