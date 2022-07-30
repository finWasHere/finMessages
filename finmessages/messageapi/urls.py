from django.urls import path #, include
from . import views

urlpatterns = [
    path("create",
        views.CreateViewSet.as_view(actions={'post': 'create'}),
        name="create-message"),
    path("messages/",
        views.ReceiveViewSet.as_view(actions={"get": "list"}),
        name="all-messages",),
    path("messages/<str:receiver>/",
        views.ReceiveViewSet.as_view(actions={"get": "list"}),
        name="messages-by-receiver",),
    # for API authorization, uncomment this and wire in user-based operations & validations
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
