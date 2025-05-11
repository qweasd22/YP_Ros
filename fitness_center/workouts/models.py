from django.db import models
from trainers.models import TrainingApplication
from clients.models import ClientProfile

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class TrainingPlan(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='plans')
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()

    def __str__(self):
        return f"План {self.client.user.full_name} от {self.start_date}"

class PlanExercise(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='plan_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    frequency_per_week = models.PositiveSmallIntegerField()
    sets = models.PositiveSmallIntegerField()
    repetitions = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('plan', 'exercise')

class DailyExerciseLog(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    heart_rate = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('client', 'date', 'exercise')
