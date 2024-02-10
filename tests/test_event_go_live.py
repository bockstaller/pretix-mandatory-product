import datetime
from django.test import TestCase
from django.utils.timezone import now
from django_scopes import scopes_disabled
from pretix.base.models import CartPosition, Event, Item, ItemCategory, Organizer, Quota
from pretix.testutils.sessions import get_cart_session_key
from .test_checkout import BaseCheckoutTestCase
from pretix_mandatory_product.signals import event_live


class EventGoLive(BaseCheckoutTestCase, TestCase):
    def test_event_live_product_active(self):
        with scopes_disabled():
            assert(event_live(self.event) == None)

    def test_event_live_product_inactive_product(self):
        with scopes_disabled():
            self.ticket_mandatory.active = False
            self.ticket_mandatory.save()
            assert(event_live(self.event) != None)

    def test_event_live_product_deleted_product(self):
        with scopes_disabled():
            self.ticket_mandatory.delete()
            assert(event_live(self.event) != None)
