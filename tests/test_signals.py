import datetime
from django.test import TestCase
from django.utils.timezone import now
from django_scopes import scopes_disabled
from pretix.base.models import CartPosition
from pretix.base.services.cart import CartError

from pretix_mandatory_product.signals import validate_cart_items

from .test_checkout import BaseCheckoutTestCase


class SignalTestCase(BaseCheckoutTestCase, TestCase):
    @scopes_disabled()
    def test_validate_cart_items_valid_combine(self):
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

        CartPosition.objects.create(
            event=self.event,
            cart_id=self.session_key,
            item=self.ticket_mandatory2,
            price=23,
            expires=now() + datetime.timedelta(minutes=10),
        )

        validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_invalid_combine(self):
        CartPosition.objects.create(
            event=self.event,
            cart_id=self.session_key,
            item=self.ticket,
            price=23,
            expires=now() + datetime.timedelta(minutes=10),
        )

        with self.assertRaises(CartError):
            validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_empty_combine(self):
        validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_valid_choose(self):
        self.event.settings["mandatory_product__combine"] = "choose"
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

        validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_invalid_choose(self):
        self.event.settings["mandatory_product__combine"] = "choose"
        CartPosition.objects.create(
            event=self.event,
            cart_id=self.session_key,
            item=self.ticket,
            price=23,
            expires=now() + datetime.timedelta(minutes=10),
        )

        with self.assertRaises(CartError):
            validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_empty_choose(self):
        self.event.settings["mandatory_product__combine"] = "choose"
        validate_cart_items(self.event, positions=CartPosition.objects.all())


class NoMandatoryProductsTestCase(BaseCheckoutTestCase, TestCase):
    @scopes_disabled()
    def setUp(self):
        super().setUp()
        self.event.settings["mandatory_product__list"] = []

    @scopes_disabled()
    def test_validate_cart_items_valid_combine(self):
        CartPosition.objects.create(
            event=self.event,
            cart_id=self.session_key,
            item=self.ticket,
            price=23,
            expires=now() + datetime.timedelta(minutes=10),
        )

        validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_invalid_combine(self):
        CartPosition.objects.create(
            event=self.event,
            cart_id=self.session_key,
            item=self.ticket_mandatory,
            price=23,
            expires=now() + datetime.timedelta(minutes=10),
        )

        validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_empty_combine(self):
        validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_valid_choose(self):
        self.event.settings["mandatory_product__combine"] = "choose"
        CartPosition.objects.create(
            event=self.event,
            cart_id=self.session_key,
            item=self.ticket,
            price=23,
            expires=now() + datetime.timedelta(minutes=10),
        )

        validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_invalid_choose(self):
        self.event.settings["mandatory_product__combine"] = "choose"
        CartPosition.objects.create(
            event=self.event,
            cart_id=self.session_key,
            item=self.ticket_mandatory,
            price=23,
            expires=now() + datetime.timedelta(minutes=10),
        )

        validate_cart_items(self.event, positions=CartPosition.objects.all())

    @scopes_disabled()
    def test_validate_cart_items_empty_choose(self):
        self.event.settings["mandatory_product__combine"] = "choose"
        validate_cart_items(self.event, positions=CartPosition.objects.all())
