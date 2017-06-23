from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout

def home_view(request):
    """Home view callable, for the home page."""
    context = {'food': 'steak'}
    return render(request, 'django_imager/home.html', context=context)


def account_view(request):
    return render(request, 'django_imager/account.html')


def profile_view(request):
    return render(request, 'django_imager/profile.html')


def logout_view(request):
    # message user or whatever
    return auth_views.logout(request)
    # user = getattr(request, 'user', None)
    # if hasattr(user, 'is_authenticated') and not user.is_authenticated:
    #     user = None
    # user_logged_out.send(sender=user.__class__, request=request, user=user)

    # # remember language choice saved to session
    # language = request.session.get(LANGUAGE_SESSION_KEY)

    # request.session.flush()

    # if language is not None:
    #     request.session[LANGUAGE_SESSION_KEY] = language

    # if hasattr(request, 'user'):
    #     from django.contrib.auth.models import AnonymousUser
    #     request.user = AnonymousUser()


# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('settings:profile')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })
