from django.utils.translation import gettext_lazy

from pretix_mandatory_product import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    name = "pretix_mandatory_product"
    verbose_name = "Mandatory Product"

    def ready(self):
        from . import signals  # NOQA

    class PretixPluginMeta:
        name = gettext_lazy("Mandatory Product")
        author = "Lukas Bockstaller"
        version = __version__
        description = gettext_lazy(
            "Forces the customer to buy at least one of a product."
        )
        category = "FEATURE"
        featured = True
        visible = True
        restricted = False
        compatibility = "pretix>=3.0"


default_app_config = "pretix_mandatory_product.PluginApp"
