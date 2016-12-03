from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import Region


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            user.team.name = user.username
            user.team.region = Region.objects.get(
                pk=settings.DEFAULT_REGION_ID)
            user.team.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'cabinet/register.html', {'form': form})
