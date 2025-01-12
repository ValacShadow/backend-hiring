from django.urls import path
from .views import SubmitJobAPIView, JobStatusAPIView, index

urlpatterns = [
    path("", index, name="index"),
    # API endpoint to submit a new job
    path('jobs/submit/', SubmitJobAPIView.as_view(), name='submit_job'),
    # API endpoint to fetch the status of a specific job queue
    path('jobs/status/<int:job_queue_id>/', JobStatusAPIView.as_view(), name='job_status'),
]
