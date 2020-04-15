from rest_framework_mongoengine import routers as merouters

from .API.views import MethodsViewSet

merouter = merouters.DefaultRouter()
merouter.register(r'methods', MethodsViewSet)

urlpatterns = [
]

urlpatterns += merouter.urls
