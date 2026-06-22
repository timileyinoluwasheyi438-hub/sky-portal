from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Department, Team, AuditLog
from .forms import TeamForm, DepartmentForm

@login_required
def dashboard(request):
    departments = Department.objects.prefetch_related('teams').all()
    recent_logs = AuditLog.objects.all()[:5]
    context = {
        'departments': departments,
        'recent_logs': recent_logs,
        'total_teams': Team.objects.filter(status='active').count(),
        'total_departments': Department.objects.count(),
    }
    return render(request, 'teams/dashboard.html', context)

@login_required
def team_list(request):
    teams = Team.objects.select_related('department', 'manager').all()
    return render(request, 'teams/team_list.html', {'teams': teams})

@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    context = {
        'team': team,
        'engineers': team.engineers.all(),
        'upstream': team.dependencies.all(),
        'downstream': team.dependents.all(),
    }
    return render(request, 'teams/team_detail.html', context)

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            AuditLog.objects.create(
                user=request.user,
                action=f"Created team '{team.name}'",
                details=f"Department: {team.department.name}"
            )
            messages.success(request, f"Team '{team.name}' created!")
            return redirect('team_detail', pk=team.pk)
    else:
        form = TeamForm()
    return render(request, 'teams/team_form.html', {'form': form, 'title': 'Create Team'})

@login_required
def team_edit(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(
                user=request.user,
                action=f"Updated team '{team.name}'",
                details=f"Status: {team.status}"
            )
            messages.success(request, f"Team '{team.name}' updated!")
            return redirect('team_detail', pk=team.pk)
    else:
        form = TeamForm(instance=team)
    return render(request, 'teams/team_form.html', {'form': form, 'title': 'Edit Team', 'team': team})

@login_required
def team_disband(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        team.status = 'disbanded'
        team.save()
        AuditLog.objects.create(user=request.user, action=f"Disbanded team '{team.name}'")
        messages.warning(request, f"Team '{team.name}' disbanded.")
        return redirect('team_list')
    return render(request, 'teams/team_confirm_disband.html', {'team': team})

@login_required
def search(request):
    query = request.GET.get('q', '')
    teams = []
    departments = []
    if query:
        teams = Team.objects.filter(
            Q(name__icontains=query) |
            Q(manager__username__icontains=query) |
            Q(manager__first_name__icontains=query) |
            Q(purpose__icontains=query)
        )
        departments = Department.objects.filter(Q(name__icontains=query))
    return render(request, 'teams/search_results.html', {
        'query': query, 'teams': teams, 'departments': departments
    })

@login_required
def audit_log(request):
    logs = AuditLog.objects.all()
    return render(request, 'teams/audit_log.html', {'logs': logs})