from django.shortcuts import render
# from django.template import loader


def home_view(request):
    """Home view callable, for the home page."""
    # template = loader.get_template('django_imager/home.html')
    # response_body = template.render()
    # return HttpResponse(response_body)
    context = {
        'food': 'steak'
    }
    return render(request, 'django_imager/home.html', context=context)


def login_view(request):
    return render(request, 'django_imager/login.html')


def account_view(request):
    return render(request, 'django_imager/account.html')
