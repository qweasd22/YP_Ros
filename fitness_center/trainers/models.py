from django.db import models
from accounts.models import User


class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role':'trainer'})
    experience_years = models.PositiveIntegerField(default=0)
    achievements = models.TextField(blank=True)

    def __str__(self):
        return self.user.full_name

class TrainingApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    )
    client = models.ForeignKey(
        'clients.ClientProfile',
        on_delete=models.CASCADE,
        related_name='applications'
    )
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='applications')
    goal = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reject_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.user.full_name} → {self.trainer.user.full_name} [{self.get_status_display()}]"
