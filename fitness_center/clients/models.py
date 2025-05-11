from django.db import models
from accounts.models import User


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role':'client'})
    trainer = models.ForeignKey(
        'trainers.TrainerProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.full_name
