"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import projectapp.views as pvs


router1 = DefaultRouter()
router1.register(r'Blogs', pvs.BlogsViewSet, basename='Blogs')

router2 = DefaultRouter()
router2.register(r'Recension', pvs.RecensionViewSet, basename='Recension')

router3 = DefaultRouter()
router3.register(r'Users', pvs.UserViewSet, basename='Users')

router4 = DefaultRouter()
router4.register(r'Comments', pvs.CommentViewSet, basename='Comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(router1.urls)),
    path("", include(router2.urls)),
    path("", include(router3.urls)),
    path("", include(router4.urls)),
    # path('signup/', pvs.signup),
    # path('<int:tokenkey>', pvs.ifTokenIsValid)
    # path('signup/', pvs.RegisterUser.as_view())

]
