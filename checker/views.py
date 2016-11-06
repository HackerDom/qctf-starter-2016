from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Task
from cabinet.models import Team


def index(request):
    tasks = Task.objects.all()
    return render(request, 'checker/index.html', {'tasks': tasks})


@login_required
@require_POST
def check_flag(request, task_id):
    team = request.user.team
    task = get_object_or_404(Task, pk=task_id)
    flag = request.POST.get('flag', '')
    status = 'ok' if task.submit_flag(team, flag) else 'wrong'
    return JsonResponse({'error': False, 'status': status})


def scoreboard(request):
    teams = Team.objects.all().order_by('-tasks_number')
    print(teams)
    return render(request, 'checker/scoreboard.html', {'teams': teams})
