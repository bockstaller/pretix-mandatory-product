from django.test import TestCase
from django_scopes import scopes_disabled

from pretix_mandatory_product.signals import event_live

from .test_checkout import BaseCheckoutTestCase


class EventGoLive(BaseCheckoutTestCase, TestCase):
    def test_event_live_product_active(self):
        with scopes_disabled():
            assert event_live(self.event) is None

    def test_event_live_product_inactive_product(self):
        with scopes_disabled():
            self.ticket_mandatory.active = False
            self.ticket_mandatory.save()
            assert event_live(self.event) is not None

    def test_event_live_product_deleted_product(self):
        with scopes_disabled():
            self.ticket_mandatory.delete()
            assert event_live(self.event) is not None
