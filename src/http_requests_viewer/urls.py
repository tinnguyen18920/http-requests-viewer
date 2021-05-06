from http_requests_viewer import views

from django.urls import path

app_name = "http_requests_viewer"

urlpatterns = [
    path("", views.TargetCreateView.as_view(), name="target_create"),

    path("agents/", views.AgentListAndCreateView.as_view(), name="agent_list"),
    path("agents/<str:pk>/delete/", views.AgentDeleteView.as_view(), name="agent_delete"),
    
    path("exclude_hosts/", views.ExcludeHostListAndCreateView.as_view(), name="exclude_host_list"),
    path("exclude_hosts/<str:pk>/delete/", views.ExcludeHostDeleteView.as_view(), name="exclude_host_delete"),
    
    path("targets/", views.TargetListView.as_view(), name="target_list"),
    path("targets/new/", views.TargetCreateView.as_view(), name="target_create"),
    path("targets/<str:pk>/", views.TargetDetailView.as_view(), name="target_detail"),
    path("targets/<str:pk>/delete/", views.TargetDeleteView.as_view(), name="target_delete"),

    path("targets/<str:pk>/requests/<str:request_id>/", views.RequestDetailView.as_view(), name="request_detail"),
    path("targets/<str:pk>/requests/<str:request_id>/response/", views.RequestResponseView.as_view(), name="request_response"),
]