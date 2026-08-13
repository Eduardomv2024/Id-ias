from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from board.api import ContactViewSet, TaskViewSet
from board import views as board_views

router = DefaultRouter()
router.register("contacts", ContactViewSet)
router.register("tasks", TaskViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("", include("board.urls")),
]
