from django.test import TestCase
from .models import Event
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse, resolve
from django.contrib.auth.models import User
import tempfile
from PIL import Image


def temporary_image():
    """ Returns a new temporary image file """

    image = Image.new("RGB", (512, 512), "white")
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file, 'jpeg')
    tmp_file.seek(0)
    return tmp_file

def populate_response(self, event, change_event):
    return self.client.put(reverse('event-detail',
                                   kwargs={'pk': event.id}),
                                   change_event,
                                   format='json')


class ModelTestCase(TestCase):
    """This class defines the test suite for the event model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.eventName = "Teste"
        self.owner = "Fulano"
        self.eventDate = "2099-12-14"
        self.eventHour = "03:03:00"
        self.organizer = "Fulano"
        self.address = "Here"
        self.eventDescription = "Chato"
        self.foods = "Comidas"
        self.drinks = "Bebidas"

        self.event = Event(eventName=self.eventName,
                           owner=self.owner,
                           eventDate=self.eventDate,
                           eventHour=self.eventHour,
                           organizer=self.organizer,
                           address=self.address,
                           eventDescription=self.eventDescription,
                           foods=self.foods,
                           drinks=self.drinks)

    def test_model_can_create_a_event(self):
        """Test the event model can create a event."""
        old_count = Event.objects.count()
        self.event.save()
        new_count = Event.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="User01")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.event_data = {'eventName': 'Teste1',
                           'owner': 'Fulano',
                           'eventDate': "2099-12-15",
                           'eventHour': "03:03:00",
                           'organizer': "Fulano",
                           'address': "Here",
                           'eventDescription': "Chato",
                           'foods': "Comidas",
                           'drinks': "Bebidas",
                           'photo': temporary_image()}
        self.response1 = self.client.post(
            reverse('event-list'),
            self.event_data,
            format="multipart")

    """ Test: Creating """

    def test_api_event_create(self):
        """Test the api has event creation capability."""
        self.assertEqual(self.response1.status_code, status.HTTP_201_CREATED)

    """ Test: Getting """

    def test_api_event_get(self):
        """Test the api can get a given event."""
        event = Event.objects.get()
        response = self.client.get(
        reverse('event-detail', kwargs={'pk': event.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, event)

    """ Test: Updating """

    def test_api_event_update(self):
        """Test the api can update a given event."""
        event = Event.objects.get()
        change_event = {'eventName': 'Mudei este campo',
                        'owner': 'Fulano',
                        'eventDate': "2099-12-13",
                        'eventHour': "03:03:00",
                        'organizer': "Fulano",
                        'address': "Here",
                        'eventDescription': "Chato",
                        'foods': "Comidas",
                        'drinks': "Bebidas"}
        response = populate_response(self, event, change_event)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """ Test the api cannot update if a required field is blank """
        change_event = {'eventName': 'Mudei este campo',
                        'owner': 'Fulano',
                        'eventDate': "2099-12-16",
                        'eventHour': "03:03:00",
                        'organizer': "",  # Organizer é obrigatório
                        'address': "Here",
                        'eventDescription': "Chato",
                        'foods': "Comidas",
                        'drinks': "Bebidas"}
        response = populate_response(self, event, change_event)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """ Test the api cannot update if linkReference field is not a URL """
        change_event = {'eventName': 'Teste',
                        'owner': 'Fulano',
                        'eventDate': "2099-12-18",
                        'eventHour': "03:03:00",
                        'organizer': "Fulano",
                        'value': 0,
                        'address': "Here",
                        'eventDescription': "Chato",
                        'foods': "Comidas",
                        'drinks': "Bebidas",
                        'linkReference': 'incorrect.com'}
        response = populate_response(self, event, change_event)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """ Test the api cannot update if linkReference field is not a URL """
        change_event = {'eventName': 'Teste',
                        'owner': 'Fulano',
                        'eventDate': "2099-12-12",
                        'eventHour': "03:03:00",
                        'organizer': "Fulano",
                        'value': 0,
                        'address': "Here",
                        'eventDescription': "Chato",
                        'foods': "Comidas",
                        'drinks': "Bebidas",
                        'linkAddress': 'incorrect.com'}
        response = populate_response(self, event, change_event)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """ Test the api cannot update if file is not a image """
        change_event = {'eventName': 'Teste',
                        'owner': 'Fulano',
                        'eventDate': "2099-12-12",
                        'eventHour': "03:03:00",
                        'organizer': "Fulano",
                        'value': 0,
                        'address': "Here",
                        'eventDescription': "Chato",
                        'foods': "Comidas",
                        'drinks': "Bebidas",
                        'photo': "teste.txt"}
        response = populate_response(self, event, change_event)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_api_event_validators(self):
            event = Event.objects.get()
            """ Test the api cannot update if date is incorret """
            change_event = {'eventName': 'Teste',
                            'owner': 'Fulano',
                            'eventDate': "2018-05-05",
                            'eventHour': "03:03:00",
                            'organizer': "Fulano",
                            'value': 0,
                            'address': "Here",
                            'eventDescription': "Chato",
                            'foods': "Comidas",
                            'drinks': "Bebidas"}
            response = populate_response(self, event, change_event)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            """ Test the api cannot update if value is negative """
            change_event = {'eventName': 'Teste',
                            'owner': 'Fulano',
                            'eventDate': "2099-12-17",
                            'eventHour': "03:03:00",
                            'organizer': "Fulano",
                            'value': -2,
                            'address': "Here",
                            'eventDescription': "Chato",
                            'foods': "Comidas",
                            'drinks': "Bebidas"}
            response = populate_response(self, event, change_event)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
