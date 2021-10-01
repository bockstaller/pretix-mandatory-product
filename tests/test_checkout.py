import datetime
from django.test import TestCase
from django.utils.timezone import now
from django_scopes import scopes_disabled
from pretix.base.models import CartPosition, Event, Item, ItemCategory, Organizer, Quota
from pretix.testutils.sessions import get_cart_session_key

from pretix_mandatory_product.views import Modes


class BaseCheckoutTestCase:
    def _set_session(self, key, value):
        session = self.client.session
        session["carts"][get_cart_session_key(self.client, self.event)][key] = value
        session.save()

    @scopes_disabled()
    def setUp(self):
        super().setUp()
        self.orga = Organizer.objects.create(name="Dummy", slug="dummy")
        self.event = Event.objects.create(
            organizer=self.orga,
            name="Dummy",
            slug="dummy",
            date_from=now(),
            live=True,
            plugins="pretix_mandatory_product",
        )
        self.category = ItemCategory.objects.create(
            event=self.event, name="Everything", position=0
        )
        self.quota_tickets = Quota.objects.create(
            event=self.event, name="Tickets", size=5
        )

        self.ticket_mandatory = Item.objects.create(
            event=self.event,
            name="Early-bird ticket",
            category=self.category,
            default_price=23,
            admission=True,
        )
        self.quota_tickets.items.add(self.ticket_mandatory)

        self.ticket_mandatory2 = Item.objects.create(
            event=self.event,
            name="Early-bird ticket",
            category=self.category,
            default_price=23,
            admission=True,
        )
        self.quota_tickets.items.add(self.ticket_mandatory2)

        self.ticket = Item.objects.create(
            event=self.event,
            name="Early-bird ticket",
            category=self.category,
            default_price=23,
            admission=True,
        )
        self.quota_tickets.items.add(self.ticket)

        self.client.get("/%s/%s/" % (self.orga.slug, self.event.slug))
        self.session_key = get_cart_session_key(self.client, self.event)
        self._set_session("email", "admin@localhost")

        self.event.settings["mandatory_product__list"] = [
            self.ticket_mandatory.id,
            self.ticket_mandatory2.id,
        ]


class CheckoutTestCase(BaseCheckoutTestCase, TestCase):
    def test_make_order_without_mandatory_product(self):
        with scopes_disabled():

            self.event.settings["mandatory_product__combine"] = Modes.CHOOSE.value

            CartPosition.objects.create(
                event=self.event,
                cart_id=self.session_key,
                item=self.ticket,
                price=23,
                expires=now() + datetime.timedelta(minutes=10),
            )
            response = self.client.get(
                "/%s/%s/checkout/questions/"
                % (self.event.organizer.slug, self.event.slug),
            )

            self.assertNotEqual(response.status_code, 200)

            self.assertRedirects(
                response,
                "/%s/%s/?require_cookie=true"
                % (self.event.organizer.slug, self.event.slug),
            )

    def test_make_order_with_mandatory_product(self):
        with scopes_disabled():

            self.event.settings["mandatory_product__combine"] = Modes.CHOOSE.value

            CartPosition.objects.create(
                event=self.event,
                cart_id=self.session_key,
                item=self.ticket_mandatory,
                price=23,
                expires=now() + datetime.timedelta(minutes=10),
            )

            response = self.client.get(
                "/%s/%s/checkout/questions/"
                % (self.event.organizer.slug, self.event.slug),
            )

            self.assertEqual(response.status_code, 200)

    def test_make_order_without_mandatory_product_combine_fail_1(self):
        with scopes_disabled():

            self.event.settings["mandatory_product__combine"] = Modes.COMBINE.value
            CartPosition.objects.create(
                event=self.event,
                cart_id=self.session_key,
                item=self.ticket,
                price=23,
                expires=now() + datetime.timedelta(minutes=10),
            )
            CartPosition.objects.create(
                event=self.event,
                cart_id=self.session_key,
                item=self.ticket_mandatory,
                price=23,
                expires=now() + datetime.timedelta(minutes=10),
            )
            response = self.client.get(
                "/%s/%s/checkout/questions/"
                % (self.event.organizer.slug, self.event.slug),
            )

            self.assertNotEqual(response.status_code, 200)

            self.assertRedirects(
                response,
                "/%s/%s/?require_cookie=true"
                % (self.event.organizer.slug, self.event.slug),
            )

    def test_make_order_with_mandatory_product_combine_fail_2(self):
        with scopes_disabled():

            self.event.settings["mandatory_product__combine"] = Modes.COMBINE.value
            CartPosition.objects.create(
                event=self.event,
                cart_id=self.session_key,
                item=self.ticket,
                price=23,
                expires=now() + datetime.timedelta(minutes=10),
            )
            CartPosition.objects.create(
                event=self.event,
                cart_id=self.session_key,
                item=self.ticket_mandatory2,
                price=23,
                expires=now() + datetime.timedelta(minutes=10),
            )

            response = self.client.get(
                "/%s/%s/checkout/questions/"
                % (self.event.organizer.slug, self.event.slug),
            )

            self.assertNotEqual(response.status_code, 200)

            self.assertRedirects(
                response,
                "/%s/%s/?require_cookie=true"
                % (self.event.organizer.slug, self.event.slug),
            )

    def test_make_order_with_mandatory_product_combine_success(self):
        with scopes_disabled():

            self.event.settings["mandatory_product__combine"] = Modes.COMBINE.value

            CartPosition.objects.create(
                event=self.event,
                cart_id=self.session_key,
                item=self.ticket_mandatory,
                price=23,
                expires=now() + datetime.timedelta(minutes=10),
            )
            CartPosition.objects.create(
                event=self.event,
                cart_id=self.session_key,
                item=self.ticket_mandatory2,
                price=23,
                expires=now() + datetime.timedelta(minutes=10),
            )

            response = self.client.get(
                "/%s/%s/checkout/questions/"
                % (self.event.organizer.slug, self.event.slug),
            )

            self.assertEqual(response.status_code, 200)
