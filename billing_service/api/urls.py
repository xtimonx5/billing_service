from django.urls import path, include

from .views import (
    RegistrationView,
    DepositView,
    TransferView,
    AccountView,
)

urlpatterns = [
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('register/', RegistrationView.as_view(), name='register'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('account/', AccountView.as_view(), name='account'),
]
