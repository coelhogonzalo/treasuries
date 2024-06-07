from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import (
    countries,
    detail_view,
    etf_aum_history,
    etfs,
    index,
    miners,
    net_flows,
)

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("treasuries/", include("treasuries.urls")),
    path("countries/", countries, name="countries"),
    path("miners/", miners, name="miners"),
    path("us-etfs/", etfs, name="us-etfs"),
    path("us-etf-aum/", etf_aum_history, name="us-etf-aum"),
    path("net-us-et-flows/", net_flows, name="net-flows"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("<str:info_url>/", detail_view, name="treasury_detail"),
]
