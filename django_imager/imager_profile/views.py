from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def home_view(request):
    """Home view callable, for the home page."""
    # template = loader.get_template('django_imager/home.html')
    # response_body = template.render()
    # return HttpResponse(response_body)
    context = {
        'food': 'steak'
    }
    return render(request, 'django_imager/home.html', context=context)


# def login_view(request):
#     return render(request, 'django_imager/login.html')


def account_view(request):
    return render(request, 'django_imager/account.html')


@csrf_exempt
def register_user(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = RegisterForm(auto_id=False)
    context['form'] = form
    return render_to_response('templates/register.htm', context, context_instance=RequestContext(request))


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})