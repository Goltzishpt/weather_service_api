from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from cities.models import City, CityTemperature


class CityAPITests(APITestCase):
    def setUp(self):
        self.city = City.objects.create(
            name="Odesa",
            description="my best some city",
        )
        self.city2 = City.objects.create(
            name="Kyiv",
            description="the big city",
        )

    def test_create_city(self):
        url = reverse("city")
        data = {"name": "Lviv", "description": "beautiful city"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Lviv")
        self.assertEqual(City.objects.count(), 3)

    def test_list_cities(self):
        url = reverse("city")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("cities", response.data)
        self.assertEqual(len(response.data["cities"]), 2)

    def test_get_city_detail(self):
        url = reverse("city-detail", args=[self.city.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.city.id))
        self.assertEqual(response.data["name"], "Odesa")

    def test_patch_city(self):
        url = reverse("city-detail", args=[self.city.id])
        data = {"description": "updated description"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.city.refresh_from_db()
        self.assertEqual(self.city.description, "updated description")

    def test_delete_city(self):
        url = reverse("city-detail", args=[self.city.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(City.objects.filter(id=self.city.id).exists())

    def test_create_city_without_name_fails(self):
        url = reverse("city")
        data = {"description": "city without name"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)



class CityTemperatureAPITests(APITestCase):
    def setUp(self):
        self.city = City.objects.create(
            name="Odesa",
            description="my best some city",
        )
        self.city2 = City.objects.create(
            name="Kyiv",
            description="the big city",
        )

    def test_set_temperature_for_city(self):
        url = reverse("set-temperature", args=[self.city.id])
        data = {"value": 12.4}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["value"], 12.4)
        self.assertEqual(CityTemperature.objects.count(), 1)
        temp = CityTemperature.objects.first()
        self.assertEqual(temp.city, self.city)
        self.assertEqual(temp.value, 12.4)

    def test_set_temperature_for_non_existing_city(self):
        url = reverse("set-temperature", args=["017a2fa4-e4c2-4704-82fe-a1edf0d4ed68"])
        City.objects.all().delete()  # гарантируем, что такого города нет
        data = {"value": 10.0}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_stats_overall_average(self):
        CityTemperature.objects.create(city=self.city, value=10.0)
        CityTemperature.objects.create(city=self.city2, value=20.0)

        url = reverse("stats")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data["average"], 15.0)

    def test_stats_for_specific_city(self):
        CityTemperature.objects.create(city=self.city, value=10.0)
        CityTemperature.objects.create(city=self.city, value=20.0)
        CityTemperature.objects.create(city=self.city2, value=30.0)

        url = reverse("stats")
        response = self.client.get(url, {"city_id": str(self.city.id)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data["average"], 15.0)

    def test_stats_invalid_city_id(self):
        url = reverse("stats")
        response = self.client.get(url, {"city_id": "invalid-uuid"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("city_id", response.data)

    def test_set_temperature_without_value_fails(self):
        url = reverse("set-temperature", args=[self.city.id])
        data = {}  # нет value
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("value", response.data)

    def test_set_temperature_with_invalid_value_type_fails(self):
        url = reverse("set-temperature", args=[self.city.id])
        data = {"value": "hot"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("value", response.data)
