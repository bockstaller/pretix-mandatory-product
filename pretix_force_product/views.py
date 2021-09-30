from collections import OrderedDict
from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.forms import SettingsForm
from pretix.base.models import Event
from pretix.base.plugins import PluginConfig
from pretix.base.settings import validate_event_settings
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin


class ForceProductSettingsForm(SettingsForm):
    forced_product__list = forms.MultipleChoiceField(
        choices=[],
        label=_("Force products"),
        required=False,
    )
    forced_product_check = forms.BooleanField(
        label=_("Enable validation"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.get("obj")
        super().__init__(*args, **kwargs)

        choices = (
            (str(i["id"]), i["name"]) for i in event.items.values("name", "id").all()
        )
        self.fields["forced_product__list"].choices = choices


class SettingsView(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = ForceProductSettingsForm
    template_name = "pretix_force_product/settings.html"
    permission = "can_change_settings"

    def get_success_url(self):
        return reverse(
            "plugins:pretix_force_product:force_product__settings",
            kwargs={
                "organizer": self.request.event.organizer.slug,
                "event": self.request.event.slug,
            },
        )
