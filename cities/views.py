import uuid

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Avg
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from cities.models import City, CityTemperature
from cities.serializers import (
    CitySerializer,
    CityTemperatureSerializer,
)


class CityListView(APIView):

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response({"cities": serializer.data})

    @swagger_auto_schema(
        request_body=CitySerializer,
        responses={201: CitySerializer}
    )
    def post(self, request):
        serializer = CitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CityDetailView(APIView):

    def get(self, request, pk):
        city = get_object_or_404(City, pk=pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CitySerializer,
        responses={200: CitySerializer}
    )
    def patch(self, request, pk):
        city = get_object_or_404(City, pk=pk)
        serializer = CitySerializer(city, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        city = get_object_or_404(City, pk=pk)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CityTemperatureView(APIView):

    @swagger_auto_schema(
        request_body=CityTemperatureSerializer,
        responses={201: openapi.Response("Created", CityTemperatureSerializer)}
    )
    def post(self, request, pk):
        city = get_object_or_404(City, pk=pk)
        serializer = CityTemperatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(city=city)
        return Response({"value": serializer.data["value"]}, status=status.HTTP_201_CREATED)


class StatsView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'city_id',
                openapi.IN_QUERY,
                description="Optional city UUID to filter average temperature by city",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={200: openapi.Response("Average temperature", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "average": openapi.Schema(type=openapi.TYPE_NUMBER, format='float')
            },
        ))}
    )
    def get(self, request):
        city_id = request.query_params.get("city_id")
        qs = CityTemperature.objects.all()

        if city_id:
            try:
                uuid.UUID(city_id)
            except ValueError:
                raise ValidationError({"city_id": "Invalid city_id format"})

            qs = qs.filter(city_id=city_id)

        avg_value = qs.aggregate(avg=Avg("value"))["avg"]
        return Response({"average": avg_value})
