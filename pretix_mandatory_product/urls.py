from django.urls import re_path

from .views import SettingsView

urlpatterns = [
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/mandatory_product/settings$",
        SettingsView.as_view(),
        name="mandatory_product__settings",
    ),
]
