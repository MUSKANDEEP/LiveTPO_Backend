from django.urls import path
from .views import (
    FeedbackCreateView, FeedbackUpdateView, FeedbackDeleteView,
    FeedbackListView, FeedbackDetailView
)

urlpatterns = [
    path('create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('update/<int:id>/', FeedbackUpdateView.as_view(), name='feedback-update'),
    path('delete/<int:id>/', FeedbackDeleteView.as_view(), name='feedback-delete'),
    path('', FeedbackListView.as_view(), name='feedback-list'),                 # GET all
    path('<int:id>/', FeedbackDetailView.as_view(), name='feedback-detail'),   # GET one
]
