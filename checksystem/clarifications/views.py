from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import UserClar


@login_required
def index(request):
    clars = UserClar.objects.filter(recipient=request.user.team)
    for clar in clars:
        clar.mark_as_read()
    return render(request, 'clarifications/index.html', {'clars': clars})


@login_required
def read_clar(request, clar_id):
    clar = get_object_or_404(UserClar, pk=clar_id, recipient=request.user.team)
    clar.mark_as_read()
    return render(request, 'clarifications/clar.html', {'clar': clar})
