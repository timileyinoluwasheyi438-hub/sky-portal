from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Engineer, Team
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
def team_details(request, pk):
    team = get_object_or_404(Team, pk=pk)
    context = {
        'team': team,
        'engineers': team.engineers.all(),
        'upstream': team.dependencies.all(),
        'downstream': team.dependents.all(),
    }
    return render(request, 'teams/team_details.html', context)

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            # === Create new department if provided ===
            new_name = form.cleaned_data.get('new_department_name')
            new_desc = form.cleaned_data.get('new_department_description')

            if new_name and new_name.strip():
                department, created = Department.objects.get_or_create(
                    name=new_name.strip(),
                    defaults={'description': new_desc or ''}
                )
                form.instance.department = department

            team = form.save()
            
            # Optional: Log the creation
            AuditLog.objects.create(
                user=request.user,
                action=f"Created new team '{team.name}'",
                details=f"Department: {team.department.name}"
            )
            
            messages.success(request, f"Team '{team.name}' created successfully!")
            return redirect('team_list')  

    else:
        form = TeamForm()

    departments = Department.objects.all()
    return render(request, 'teams/team_form.html', {
        'form': form,
        'departments': departments,
        'title': 'Create New Team'
    })


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


@login_required
def add_engineer(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        email = request.POST.get('email')
        Engineer.objects.create(team=team, name=name, role=role, email=email)
    return redirect('team_detail', pk=pk)