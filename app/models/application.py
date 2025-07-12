from django.db import models
from .base import BaseModel
from .user import User

class Application(BaseModel):
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
    notes = models.TextField(blank=True)
    job_url = models.URLField(blank=True)
    contact_person = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        db_table = 'applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.position} at {self.company}" 