from django.contrib import admin
from django.urls import path, include

from schema_graph.views import Schema

urlpatterns = [
    path('', include('frontend.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path("schema/", Schema.as_view()),
]
