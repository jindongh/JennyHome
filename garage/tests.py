from django.test import TestCase

from models import GarageOp
from views import *
from views import _getDoorState
from views import _getNextDoorState

# Create your tests here.
class GarageTest(TestCase):
    def test_State(self):
        # init state
        initState = _getDoorState()
        self.assertIs(initState, DOOR_CLOSE)
        # new state
        newState = _getNextDoorState(initState)
        self.assertIs(newState, DOOR_OPEN)

    def testPage(self):
        response = self.client.get('/garage/')
        self.assertContains(response, 'Garage State')
