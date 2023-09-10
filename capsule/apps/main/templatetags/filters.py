from django import template


# Create register instance
register = template.Library()


@register.filter
def split_card(value):
    return "{} {} {} {}".format(value[:4], value[4:8], value[8:12], value[12:])


@ register.filter
def hidden_card(value):
    return value.replace(value[5:14], "**** ****")


@ register.filter
def split_phone(value):
    return "{} {} {}".format(value[:4], value[4:7], value[7:])


@ register.filter
def hidden_phone(value):
    return value.replace(value[5:8], "***")
