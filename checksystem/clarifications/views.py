from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import UserClar


@login_required
def index(request):
    clars = UserClar.objects.all()
    return render(request, 'clarifications/index.html', {'clars': clars})


@login_required
def read_clar(request, clar_id):
    clar = get_object_or_404(UserClar, pk=clar_id, recipient=request.user.team)
    clar.read()
    return render(request, 'clarifications/clar.html', {'clar': clar})
