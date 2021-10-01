from django.conf.urls import url

from .views import SettingsView

urlpatterns = [
    url(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/mandatory_product/settings$",
        SettingsView.as_view(),
        name="mandatory_product__settings",
    ),
]
