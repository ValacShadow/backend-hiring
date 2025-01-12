from celery import shared_task
from django.apps import apps
from time import sleep
import logging

from website.models import JobQueue, Site, UserRecords

logger = logging.getLogger(__name__)

# Task Registry (Mapping Task Names to Functions)
TASK_REGISTRY = {
    "task_01": "website.tasks.task_01",
    "task_02": "website.tasks.task_02",
    "task_03": "website.tasks.task_03",
    "task_04": "website.tasks.task_04",
    "task_05": "website.tasks.task_05",
}

from celery.exceptions import Retry

@shared_task(bind=True, max_retries=5, default_retry_delay=10)  # Exponential backoff retry
def execute_job(self, job_queue_id):
    job_queue = None  # Initialize job_queue here to prevent UnboundLocalError

    try:
        logger.info(f"Executing job {job_queue_id}")
        sleep(5)

        # Attempt to retrieve the job queue
        try:
            job_queue = JobQueue.objects.get(id=job_queue_id)
            logger.info(f"Job {job_queue_id} status: {job_queue.status}")
        except JobQueue.DoesNotExist:
            # Handle the case where the JobQueue doesn't exist
            logger.error(f"JobQueue with ID {job_queue_id} does not exist.")
            raise Exception(f"JobQueue with ID {job_queue_id} does not exist.")

        # Proceed only if job_queue was found
        if job_queue:
            job_queue.status = JobQueue.IN_PROGRESS
            job_queue.save()

            site_id = job_queue.site_id
            task_name = job_queue.job.name

            # Dynamically call the task if found in the registry
            if task_name in TASK_REGISTRY:
                module_name, func_name = TASK_REGISTRY[task_name].rsplit(".", 1)
                module = __import__(module_name, fromlist=[func_name])
                task_function = getattr(module, func_name)

                logger.info(f"Executing {task_name} for site ID {site_id}")
                success = task_function(site_id)

                if success:
                    job_queue.status = JobQueue.COMPLETED
                else:
                    job_queue.status = JobQueue.FAILED
            else:
                logger.error(f"Task {task_name} not found in registry")
                job_queue.status = JobQueue.FAILED

    except Exception as e:
        logger.error(f"Error executing job {job_queue_id}: {e}")

        # Ensure job_queue is not None before trying to save
        if job_queue:
            job_queue.status = JobQueue.FAILED

            # Retry with exponential backoff
            try:
                raise self.retry(exc=e)
            except Retry as retry_error:
                logger.warning(f"Retrying job {job_queue_id}, retry count: {self.request.retries}")
                job_queue.status = JobQueue.PENDING

    finally:
        # Save job_queue only if it's not None
        if job_queue:
            job_queue.save()


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
