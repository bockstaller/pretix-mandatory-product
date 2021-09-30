from django import forms
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
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

settings_hierarkey.add_default("forced_product__list", [], list)


@receiver(validate_cart, dispatch_uid="force_product")
def register_contact_form_fields(sender, **kwargs):
    req_product = sender.settings["forced_product__list"]

    item_ids = [i["item__id"] for i in kwargs["positions"].values("item__id")]
    for r in req_product:
        if r not in item_ids:
            raise CartError(
                _(error_messages["min_items_per_product"])
                % {
                    "min": 1,
                    "product": sender.items.get(id=r).name,
                }
            )


@receiver(nav_event_settings, dispatch_uid="force_product")
def navbar_settings(sender, request, **kwargs):
    url = resolve(request.path_info)
    return [
        {
            "label": _("Force Product Settings"),
            "url": reverse(
                "plugins:pretix_force_product:force_product__settings",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_force_product"
            and url.url_name == "force_product__settings",
        }
    ]
