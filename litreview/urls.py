
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

import authentication.views
import siteweb.views
from siteweb.views import Createticket, Subscription, Updateticket, Deleteticket, Updatereview, Deletereview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('flux/', siteweb.views.flux, name='flux'),
    path('posts/', siteweb.views.feed, name='posts'),
    path('creation-ticket/', Createticket.as_view(), name='creation-ticket'),
    path('modifier-ticket/<int:pk>', Updateticket.as_view(), name='modifier-ticket'),
    path('supprimer-ticket/<int:pk>', Deleteticket.as_view(), name='supprimer-ticket'),
    path('abonnements/', Subscription.as_view(), name='abonnements'),
    path('desabonnement/<str:pk>/', siteweb.views.desabonner, name="desabonner"),
    path('abonner/<str:pk>/', siteweb.views.abonner, name="abonner"),
    path('creation-critique/', siteweb.views.createreview, name="creation-critique"),
    path('demande-critique/<int:pk>/', siteweb.views.demandreview, name="demande-critique"),
    path('modifier-critique/<int:pk>', Updatereview.as_view(), name='modifier-critique'),
    path('supprimer-critique/<int:pk>', Deletereview.as_view(), name='supprimer-critique'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
