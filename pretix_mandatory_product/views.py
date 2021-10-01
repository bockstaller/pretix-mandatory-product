from django import forms
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from i18nfield.forms import I18nFormField, I18nTextInput
from pretix.base.forms import SettingsForm
from pretix.base.models import Event
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin


class MandatoryProductSettingsForm(SettingsForm):
    mandatory_product__list = forms.MultipleChoiceField(
        choices=[],
        label=_("Mandatory products"),
        required=False,
        widget=CheckboxSelectMultiple,
    )

    mandatory_product__combine = forms.ChoiceField(
        choices=[
            ("combine", _("All mandatory products must be bought")),
            ("choose", _("At least one of the mandatory products must be bought")),
        ],
        label=_("Combine or choose products"),
        required=False,
        widget=RadioSelect,
    )

    mandatory_product__note = I18nFormField(
        label=_("Customer visible note"),
        required=False,
        widget=I18nTextInput,
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.get("obj")
        super().__init__(*args, **kwargs)

        choices = (
            (str(i["id"]), i["name"]) for i in event.items.values("name", "id").all()
        )
        self.fields["mandatory_product__list"].choices = choices


class SettingsView(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = MandatoryProductSettingsForm
    template_name = "pretix_mandatory_product/settings.html"
    permission = "can_change_settings"

    def get_success_url(self):
        return reverse(
            "plugins:pretix_mandatory_product:mandatory_product__settings",
            kwargs={
                "organizer": self.request.event.organizer.slug,
                "event": self.request.event.slug,
            },
        )
