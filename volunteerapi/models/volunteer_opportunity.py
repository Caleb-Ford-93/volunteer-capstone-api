from django.db import models


class VolunteerOpportunity(models.Model):
    volunteer = models.ForeignKey(
        "Volunteer", on_delete=models.CASCADE, related_name="volunteers"
    )
    opportunity = models.ForeignKey(
        "Opportunity", on_delete=models.CASCADE, related_name="opportunities"
    )
