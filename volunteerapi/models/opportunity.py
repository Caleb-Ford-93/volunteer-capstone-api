from django.db import models


class Opportunity(models.Model):
    title = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    description = models.CharField(max_length=800)
    start_date = models.DateField()
    end_date = models.DateField()
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="organization"
    )
    skills = models.ManyToManyField("Skill", related_name="opportunities")
