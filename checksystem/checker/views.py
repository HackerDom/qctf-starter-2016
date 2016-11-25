from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, Http404
from django.db.models import Count
from .models import Task, Hint
from cabinet.models import Team


@login_required
def index(request):
    tasks = Task.objects.all()
    return render(request, 'checker/index.html', {'tasks': tasks})


@login_required
@require_POST
def check_flag(request, task_id):
    team = request.user.team
    task = get_object_or_404(Task, pk=task_id)
    flag = request.POST.get('flag', '')
    result = task.submit_flag(team, flag)
    result.update({'flags': team.tasks.count(), 'balance': team.balance})
    return JsonResponse(result)


def scoreboard(request):
    teams = Team.objects.filter(is_visible=True).order_by('-balance')
    return render(request, 'checker/scoreboard.html', {'teams': teams})


@login_required
def hints(request):
    hints = Hint.objects.all()
    # tasks = Task.objects.all()
    return render(request, 'checker/hints.html', {'hints': hints})


@login_required
@require_POST
def buy_hint(request, hint_id):
    team = request.user.team
    hint = get_object_or_404(Hint, pk=hint_id)
    task = hint.task
    if hint.is_bought(team):
        return JsonResponse({'error': False, 'balance': team.balance,
                             'hint': hint.get_hint_text(team)})

    if task.is_solved(team):
        raise Http404

    hint.buy(team)
    return JsonResponse({'error': False, 'balance': team.balance,
                         'hint': hint.get_hint_text(team)})
