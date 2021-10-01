from django import forms
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from pretix.base.services.cart import CartError, error_messages
from pretix.base.settings import settings_hierarkey
from pretix.base.shredder import BaseDataShredder
from pretix.base.signals import (
    register_data_exporters,
    register_data_shredders,
    register_payment_providers,
    validate_cart,
)

from pretix.control.signals import nav_event_settings
from pretix.base.signals import event_live_issues
from pretix.base.i18n import LazyLocaleException, language, LazyI18nString
from .views import Modes

settings_hierarkey.add_default("mandatory_product__list", [], list)
settings_hierarkey.add_default("mandatory_product__combine", Modes.COMBINE.value, int)


@receiver(validate_cart, dispatch_uid="mandatory_product")
def register_contact_form_fields(sender, **kwargs):

    req_product = set([int(i) for i in sender.settings["mandatory_product__list"]])
    item_ids = set([i["item__id"] for i in kwargs["positions"].values("item__id")])

    if sender.settings["mandatory_product__combine"] == Modes.COMBINE.value:
        if not req_product.issubset(item_ids):  #
            product_names = [
                r.name for r in sender.items.filter(id__in=req_product).all()
            ]

            raise CartError(
                _(
                    "You need to buy at least %(min)s of each of these products: %(product)s. %(note)s "
                )
                % {
                    "min": 1,
                    "product": ", ".join([str(p) for p in product_names]),
                    "note": sender.settings.get(
                        "mandatory_product__note", default=" ", as_type=LazyI18nString
                    ),
                }
            )
        return
    else:
        for r in req_product:
            if r in item_ids:
                return

        raise CartError(
            _(error_messages["min_items_per_product"])
            % {
                "min": 1,
                "product": sender.items.get(id=r).name,
            }
        )


@receiver(nav_event_settings, dispatch_uid="mandatory_product")
def navbar_settings(sender, request, **kwargs):
    url = resolve(request.path_info)
    return [
        {
            "label": _("Mandatory Products"),
            "url": reverse(
                "plugins:pretix_mandatory_product:mandatory_product__settings",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_mandatory_product"
            and url.url_name == "mandatory_product__settings",
        }
    ]


@receiver(event_live_issues, dispatch_uid="mandatory_product")
def event_live(sender, **kwargs):
    mandatory_products_setting = [
        int(x) for x in sender.settings["mandatory_product__list"]
    ]

    mandatory_inactive_products = (
        sender.items.filter(id__in=mandatory_products_setting)
        .filter(active=False)
        .all()
    )

    if len(mandatory_inactive_products) != 0:
        return _("You force customers to buy a product that is currently inactive.")
