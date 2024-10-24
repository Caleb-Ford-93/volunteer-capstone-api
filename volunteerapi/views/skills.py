from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from volunteerapi.models import Skill, Volunteer, Opportunity, Volunteer_Skill
from rest_framework.decorators import action


class SkillViewSet(viewsets.ViewSet):
    def list(self, request):
        """Method for listing all skills"""
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Method for Creating a new skill"""
        skill = Skill.objects.create(name=request.data["name"])
        serializer = SkillSerializer(skill)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["get", "post", "delete"], detail=False)
    def volunteer(self, request):

        current_user = request.user
        volunteer = Volunteer.objects.get(user=current_user)

        if request.method == "GET":
            """Method for getting all skills a volunteer has"""
            skills = volunteer.skills.all()
            serializer = SkillSerializer(skills, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "POST":
            """Method for adding a skill to a volunteer"""
            skill_to_add = Skill.objects.get(pk=request.data["skillId"])
            Volunteer_Skill.objects.create(
                skill=skill_to_add,
                volunteer=volunteer,
            )
            return Response({}, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            """Method for removing a skill from a volunteer"""
            skill_to_remove = Skill.objects.get(pk=request.data["skillId"])
            rel_to_remove = Volunteer_Skill.objects.get(
                skill=skill_to_remove, volunteer=volunteer
            )
            rel_to_remove.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=["get", "post", "delete"], detail=False)
    def opportunity(self, request):

        current_user = request.user
        opportunity = Opportunity.objects.get(pk=request.data["opportunityId"])

        if request.method == "GET":
            skills = opportunity.skills.all()
            serializer = SkillSerializer(skills, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = (
            "id",
            "name",
        )
