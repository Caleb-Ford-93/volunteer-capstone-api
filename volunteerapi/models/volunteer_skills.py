from django.db import models


class Volunteer_Skill(models.Model):
    volunteer = models.ForeignKey("volunteer", on_delete=models.CASCADE)
    skill = models.ForeignKey("skill", on_delete=models.CASCADE)
