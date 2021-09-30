from django.conf.urls import url

from .views import SettingsView

urlpatterns = [
    url(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/force_product/settings$",
        SettingsView.as_view(),
        name="force_product__settings",
    ),
]
