import datetime
from django.test import TestCase
from django_scopes import scopes_disabled
from pretix.base.models import Event, Item

from .test_checkout import BaseCheckoutTestCase


class EventCloneTestCase(BaseCheckoutTestCase, TestCase):
    def test_clone_shop(self):
        with scopes_disabled():
            copied_event = Event.objects.create(
                organizer=self.orga,
                name="Dummy2",
                slug="dummy2",
                date_from=datetime.datetime(
                    2022, 4, 15, 9, 0, 0, tzinfo=datetime.timezone.utc
                ),
            )
            copied_event.copy_data_from(self.event)
            copied_event.refresh_from_db()
            self.event.refresh_from_db()

            # assert that mandatory products are set
            assert copied_event.settings["mandatory_product__list"]

            # assert that the mandatory product ids are not pointing to the old ids
            mandatory_products = copied_event.settings["mandatory_product__list"]
            existing_products = Item.objects.filter(event=copied_event)
            for mandatory_product in mandatory_products:
                assert mandatory_product in [e_p.id for e_p in existing_products]
