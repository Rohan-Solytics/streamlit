from django.urls import path
from .views import CheckCertificateStatus, CreateSSLCertificate,trigger_jenkins,check_build

urlpatterns = [
    path('create-ssl/', CreateSSLCertificate.as_view(), name='create-ssl'),
    path('check-ssl-status/', CheckCertificateStatus.as_view(), name='check-status'),
    path('trigger-jenkins/', trigger_jenkins.as_view(), name='check-status'),
    path('check-jenkins-status/', check_build.as_view(), name='check-status'),
]