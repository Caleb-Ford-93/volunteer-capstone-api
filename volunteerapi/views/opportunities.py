from volunteerapi.models import (
    Opportunity,
    Organization,
    VolunteerOpportunity,
    Volunteer,
)
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework import serializers, permissions
from rest_framework.response import Response


class OpportunityViewSet(viewsets.ViewSet):

    def list(self, request):

        current_user = request.user

        if current_user.is_staff:
            return Response(
                {},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        opportunities = Opportunity.objects.all().order_by("start_date")
        serializer = OpportunitySerializer(
            opportunities, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        try:
            opportunity = Opportunity.objects.get(pk=pk)
            serializer = OpportunitySerializer(
                opportunity, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Opportunity.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        current_user = request.user

        if current_user.is_staff:
            organization = current_user.organization
            opportunity = Opportunity.objects.create(
                title=request.data.get("title"),
                location=request.data.get("location"),
                description=request.data.get("description"),
                start_date=request.data.get("start_date"),
                end_date=request.data.get("end_date"),
                organization=organization,
            )
            return Response({}, status=status.HTTP_201_CREATED)
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        current_user = request.user
        if current_user.is_staff:
            try:
                opportunity = Opportunity.objects.get(pk=pk)
                if opportunity.organization == current_user.organization:
                    opportunity.title = request.data["title"]
                    opportunity.location = request.data["location"]
                    opportunity.description = request.data["description"]
                    opportunity.start_date = request.data["start_date"]
                    opportunity.end_date = request.data["end_date"]
                    opportunity.save()
                    return Response({}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(
                        "That's not your opportunity to modify!",
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except Opportunity.DoesNotExist as ex:
                return Response({}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        current_user = request.user
        if current_user.is_staff:
            try:
                opportunity = Opportunity.objects.get(pk=pk)
                if opportunity.organization == current_user.organization:
                    opportunity.delete()
                    return Response({}, status=status.HTTP_200_OK)
                else:
                    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
            except Opportunity.DoesNotExist as ex:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class OpportunityOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "description", "location"]


class OpportunitySerializer(serializers.ModelSerializer):
    organization = OpportunityOrganizationSerializer(many=False, read_only=True)
    is_attending = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "title",
            "location",
            "description",
            "start_date",
            "end_date",
            "organization",
            "is_attending",
        ]

    def get_is_attending(self, obj):
        user = self.context["request"].user
        try:
            volunteer = user.volunteer
            return bool(
                VolunteerOpportunity.objects.filter(
                    volunteer=volunteer, opportunity=obj
                ).exists()
            )
        except (Volunteer.DoesNotExist, AttributeError):
            return False
