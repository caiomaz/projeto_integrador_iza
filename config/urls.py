from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Manda as requisições para /admin/ para o admin.site.urls
    path('', include('app.urls')), # Manda as requisições para qualquer rota que não seja /admin/ para o app.urls
]
