import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse
from django.db import transaction

from .models import Site, Job, JobQueue
from .tasks import execute_job

logger = logging.getLogger(__name__)


def index(request):
    return JsonResponse({"message": "Hello, world!"})

class SubmitJobAPIView(APIView):
    def post(self, request):
        site_id = request.POST.get("site_id")
        job_name = request.POST.get("job_name")

        try:
            site = Site.objects.get(id=int(site_id))  # Convert site_id to integer before querying site_id
            job = Job.objects.get(name=job_name)
            job_queue = JobQueue.objects.create(site=site, job=job)
            
            # Calculate estimated time and classify worker
            job_queue.calculate_estimated_time()
            worker_type = job_queue.classify_worker()

            # Update job_queue with estimated time and worker type
            job_queue.estimated_time = job_queue.calculate_estimated_time()
            job_queue.worker_type = worker_type
            job_queue.save()

            # Get the worker's queue based on worker_type
            worker_queue = job_queue.worker_type
            logger.info(f"Wsite.can_schedule_task: {site.can_schedule_task}")
            if job_queue.site.can_schedule_task:
                # Schedule the job for execution on the correct worker
                logger.info(f"Job {job_queue.id} scheduled for execution on worker {worker_queue}")
                execute_job.apply_async(args=[job_queue.id], queue=worker_queue)

            # transaction.on_commit(lambda: execute_job.apply_async(args=[job_queue.id], queue=worker_queue))

            # execute_job(job_queue_id=job_queue.id)
            
            return Response({"message": "Job submitted", "job_queue_id": job_queue.id})
        
        except Site.DoesNotExist:
            return Response({"error": "Invalid site ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Job.DoesNotExist:
            return Response({"error": "Invalid job name"}, status=status.HTTP_400_BAD_REQUEST)


class JobStatusAPIView(APIView):
    def get(self, request, job_queue_id):
        try:
            job_queue = JobQueue.objects.get(id=job_queue_id)
            return Response({
                "job_queue_id": job_queue.id,
                "site": job_queue.site.name,
                "job": job_queue.job.name,
                "status": job_queue.status,
            })
        except JobQueue.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
