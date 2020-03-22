from django.contrib import admin
from django.urls import path, include

# from frontend.views import login

from schema_graph.views import Schema

urlpatterns = [
    path('', include(('frontend.urls', 'frontend'), namespace='frontend')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),

    # Django-registration-redux MAGIC
    path('accounts/', include('registration.backends.default.urls')),


    path("schema/", Schema.as_view()),
]
