from time import sleep
import time
import logging

from celery import shared_task
from celery.exceptions import Retry
from django.apps import apps

from website.models import JobQueue, Site, UserRecords

logger = logging.getLogger(__name__)

def task_01(site_id: int):
    TIME_MULTIPLIER = 0.001 # very fast execution per record
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 01: {} processed".format(record.name))
    return True


def task_02(site_id: int):
    TIME_MULTIPLIER = 0.01
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 02: {} processed".format(record.name))
    return True


def task_03(site_id: int):
    TIME_MULTIPLIER = 0.1
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 03: {} processed".format(record.name))
    return True


def task_04(site_id: int):
    TIME_MULTIPLIER = 1
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 04: {} processed".format(record.name))
    return True


def task_05(site_id: int):
    TIME_MULTIPLIER = 10
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 05: {} processed".format(record.name))
    return True


TASK_REGISTRY = {
    "task_01": task_01,
    "task_02": task_02,
    "task_03": task_03,
    "task_04": task_04,
    "task_05": task_05,
}


@shared_task(bind=True, max_retries=5, default_retry_delay=10)
def execute_job(self, job_queue_id):
    job_queue = None
    try:
        logger.info(f"Executing job {job_queue_id}")

        # Attempt to retrieve the job queue
        job_queue = JobQueue.objects.get(id=job_queue_id)
        logger.info(f"Job {job_queue_id} status: {job_queue.status}")

        # Update site quota
        site = job_queue.site
        site.quota_usage += 1
        site.save()

        job_queue.status = JobQueue.IN_PROGRESS
        job_queue.save()

        site_id = job_queue.site_id
        task_name = job_queue.job.name

        # Dynamically call the task if found in the registry
        if task_name in TASK_REGISTRY:
            task_function = TASK_REGISTRY[task_name]
            # logger.info(f"Task {task_name} found in registry")
            logger.info(f"Executing {task_name} for site ID {site_id}")
            # Use Celery task delay to trigger the task asynchronously
            result = task_function(site_id)  # Asynchronous task trigger
            # Optionally, track task status here if needed (using AsyncResult)
            job_queue.status = JobQueue.COMPLETED if result else JobQueue.FAILED
        else:
            logger.error(f"Task {task_name} not found in registry")
            job_queue.status = JobQueue.FAILED

    except Exception as e:
        logger.error(f"Error executing job {job_queue_id}: {e}")

        if job_queue:
            job_queue.status = JobQueue.FAILED

        # Retry with exponential backoff
        try:
            raise self.retry(exc=e)
        except Retry:
            logger.warning(f"Retrying job {job_queue_id}, retry count: {self.request.retries}")
            if job_queue:
                job_queue.status = JobQueue.PENDING

    finally:
        if job_queue:
            job_queue.save()
            site = job_queue.site
            site.quota_usage -= 1  # Decrement quota usage after job completion
            site.save()


@shared_task(bind=True, max_retries=2, default_retry_delay=10)
def pick_pending_jobs(self):
    """
    Task to pick pending JobQueue items and schedule their execution.
    This task runs every 1 minute.
    """
    try:
        logger.info("Picking up pending jobs...")
        
        # Fetch pending jobs ordered by creation time
        pending_jobs = JobQueue.objects.filter(status=JobQueue.PENDING).order_by("created_at")
        
        if not pending_jobs.exists():
            logger.info("No pending jobs found.")
            return
        
        for job_queue in pending_jobs:
            # Check if the site's quota allows scheduling
            if job_queue.site.can_schedule_task:
                logger.info(f"Scheduling job {job_queue.id} for execution.")
                # Trigger the `execute_job` task asynchronously
                worker_queue = job_queue.worker_type
                execute_job.apply_async(args=[job_queue.id], queue=worker_queue)
            else:
                logger.warning(f"Job {job_queue.id} skipped: Quota exceeded for site {job_queue.site.id}.")
    
    except Exception as e:
        logger.error(f"Error picking pending jobs: {e}")
