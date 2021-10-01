from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


class PluginApp(PluginConfig):
    name = "pretix_mandatory_product"
    verbose_name = "Mandatory Product"

    class PretixPluginMeta:
        name = gettext_lazy("Mandatory Product")
        author = "Lukas Bockstaller"
        description = gettext_lazy(
            "Forces the customer to buy at least one of a product."
        )
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=3.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretix_mandatory_product.PluginApp"
