from django.db import models
from .user import User

class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'Applied', 'Applied'
        INTERVIEW = 'Interview', 'Interview'
        REJECTED = 'Rejected', 'Rejected'
        ACCEPTED = 'Accepted', 'Accepted'

    class JobType(models.TextChoices):
        FULL_TIME = 'Full-time', 'Full-time'
        PART_TIME = 'Part-time', 'Part-time'
        CONTRACT = 'Contract', 'Contract'
        INTERNSHIP = 'Internship', 'Internship'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    applied_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED
    )
    interview_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
        default=JobType.FULL_TIME
    )

    def __str__(self):
        return f"{self.position} at {self.company}" 

    class Meta:
        db_table = 'application'