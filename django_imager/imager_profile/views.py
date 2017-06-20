from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def home_view(request):
    """Home view callable, for the home page."""
    import pdb; pdb.set_trace()
    template = loader.get_template('django_imager/home.html')
    response_body = template.render()
    return HttpResponse(response_body)