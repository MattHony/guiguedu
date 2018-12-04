"""GuLiEdu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include


# xadmin
import xadmin
# xadmin.autodiscover()

# from xadmin.plugins import xversion
# xversion.register_models()

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    # re_path('^', include('users.urls', namespace='users')),
    # re_path('^', include('courses.urls', namespace='courses')),
    # re_path('^', include('operations.urls', namespace='operations')),
    # re_path('^', include('orgs.urls', namespace='orgs')),
    url(r'^users/', include(('users.urls', 'users'), namespace='users')),
    url(r'^courses/', include(('courses.urls', 'courses'), namespace='courses')),
    url(r'^operations/', include(('operations.urls', 'operations'), namespace='operations')),
    url(r'^orgs/', include(('orgs.urls', 'orgs'), namespace='orgs')),
]

