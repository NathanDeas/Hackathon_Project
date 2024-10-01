from django.urls import path
from hack_app import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("test_sum/", views.testing_summaries, name="test_sum"),
    path("scrape_data/", views.scrape_data, name="scrape_data"),
]