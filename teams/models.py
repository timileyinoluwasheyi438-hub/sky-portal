from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('restructured', 'Restructured'),
        ('disbanded', 'Disbanded'),
    ]
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teams')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_teams')
    purpose = models.TextField()
    responsibilities = models.TextField(blank=True)
    slack_channel = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    repo_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Engineer(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='engineers')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

class Dependency(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='dependencies')
    depends_on = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='dependents')

    class Meta:
        unique_together = ('team', 'depends_on')

    def __str__(self):
        return f"{self.team.name} depends on {self.depends_on.name}"

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=300)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.action}"