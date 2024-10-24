from django.db import models


class Opportunity_Skill(models.Model):
    opportunity = models.ForeignKey("opportunity", on_delete=models.CASCADE)
    skill = models.ForeignKey("skill", on_delete=models.CASCADE)
