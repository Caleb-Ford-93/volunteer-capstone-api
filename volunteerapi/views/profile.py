from volunteerapi.models import (
    Opportunity,
    Organization,
    VolunteerOpportunity,
    Volunteer,
)
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .opportunities import OpportunitySerializer
from .skills import SkillSerializer


class ProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        current_user = request.user
        if current_user.is_staff:
            serializer = OrganizationProfileSerializer(current_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = VolunteerProfileSerializer(current_user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get", "post", "delete"], detail=False)
    def volunteer(self, request):
        """Methods for manipulating opportunities a volunteer has signed up for"""
        current_user = request.user
        volunteer = Volunteer.objects.get(user=current_user)
        if request.method == "GET":
            """GET all opportunities a volunteer has signed up for"""
            try:
                opportunities_signed_up_for = (
                    VolunteerOpportunity.objects.filter(volunteer=volunteer)
                    .select_related("opportunity")
                    .order_by("opportunity__start_date")
                )
                serializer = VolunteerOpportunitySerializer(
                    opportunities_signed_up_for, many=True, context={"request": request}
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as ex:
                return Response(
                    {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        if request.method == "POST":
            """CREATE a new relationship between opportunity and volunteer (volunteer signing up for)"""
            try:
                opportunity_to_sign_up_for = Opportunity.objects.get(
                    pk=request.data["opportunityId"]
                )
            except Opportunity.DoesNotExist as ex:
                return Response({"error": str(ex)}, status=status.HTTP_404_NOT_FOUND)

            try:
                volunteer_opportunity = VolunteerOpportunity.objects.create(
                    volunteer=volunteer,
                    opportunity=opportunity_to_sign_up_for,
                )
                serializer = VolunteerOpportunitySerializer(
                    volunteer_opportunity, many=False, context={"request": request}
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response(
                    {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        if request.method == "DELETE":
            """Method for deleting the relationship between Opportunity and Volunteer"""
            try:
                opportunity_to_remove = Opportunity.objects.get(
                    pk=request.data["opportunityId"]
                )
            except Opportunity.DoesNotExist as ex:
                return Response({"error": str(ex)}, status=status.HTTP_404_NOT_FOUND)
            try:
                rel_to_delete = VolunteerOpportunity.objects.get(
                    volunteer=volunteer, opportunity=opportunity_to_remove
                )
                rel_to_delete.delete()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response(
                    {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=["get"], detail=False)
    def organization(self, request):
        """Method for viewing opportunities an organization has created"""
        current_user = request.user
        organization = Organization.objects.get(user=current_user)
        try:
            organization_opportunities = Opportunity.objects.filter(
                organization=organization
            )
            serializer = OpportunitySerializer(
                organization_opportunities, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VolunteerSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Volunteer
        fields = (
            "phone_number",
            "location",
            "skills",
        )


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = (
            "name",
            "location",
            "description",
        )


class VolunteerProfileSerializer(serializers.ModelSerializer):

    volunteer = VolunteerSerializer(many=False)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "volunteer",
        )
        depth = 1


class OrganizationProfileSerializer(serializers.ModelSerializer):

    organization = OrganizationSerializer(many=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "organization",
        )
        depth = 1


class VolunteerOpportunitySerializer(serializers.ModelSerializer):

    opportunity = OpportunitySerializer()

    class Meta:
        model = VolunteerOpportunity
        fields = (
            "id",
            "opportunity",
        )
