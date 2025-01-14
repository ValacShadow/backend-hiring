from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = "website"

    def ready(self):
        import logging
        logger = logging.getLogger(__name__)

        try:
            from django_celery_beat.models import PeriodicTask, IntervalSchedule

            # Avoid creating duplicate tasks
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.MINUTES,
            )
            if created:
                logger.info("Interval schedule created.")

            task, created = PeriodicTask.objects.get_or_create(
                interval=schedule,
                name="Pick Pending Jobs",
                task="website.tasks.pick_pending_jobs",
            )
            if created:
                logger.info("Periodic task 'Pick Pending Jobs' created.")
            else:
                logger.info("Periodic task 'Pick Pending Jobs' already exists.")
        except Exception as e:
            logger.error(f"Error while setting up periodic task: {e}")
