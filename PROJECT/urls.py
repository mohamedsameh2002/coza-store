from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [path("i18n/", include("django.conf.urls.i18n")),]
urlpatterns += i18n_patterns(
    path('',views.home,name='home'),
    path('sammor/', admin.site.urls),
    path('about/',views.ABOUT,name='about'),
    path('help/',views.HELP,name='help'),
    path('products/',include('store.urls')),
    path('cart/',include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('paypal/', include('paypal.standard.ipn.urls')),


)




urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404='PROJECT.views.error_404_page'