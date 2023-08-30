from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('products/',include('store.urls')),
    path('cart/',include('cart.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('orders/', include('orders.urls')),
)



urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
