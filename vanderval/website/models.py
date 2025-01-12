from django.db import models

RECORD_MAP = {
    1: 10000,
    2: 50000,
    3: 200000,
}

# Create your models here.
class Site(models.Model):
    RECORD_CAPACITY_LOW = 1  # user records between 500-10000
    RECORD_CAPACITY_MEDIUM = 2  # user records between 10000-50000
    RECORD_CAPACITY_HIGH = 3  # user records between 50000-200000

    RECORD_CAPACITY_CHOICES = (
        (RECORD_CAPACITY_LOW, "Low"),
        (RECORD_CAPACITY_MEDIUM, "Medium"),
        (RECORD_CAPACITY_HIGH, "High"),
    )

    name = models.CharField(unique=True, max_length=100)
    domain = models.URLField(null=True, blank=True)
    url = models.URLField(unique=True)
    description = models.TextField()
    record_capicity = models.IntegerField(choices=RECORD_CAPACITY_CHOICES)


# you can choose to reuse the User model from django.contrib.auth.models
class UserRecords(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # do not count for active records if false


class Job(models.Model):
    TASK_TYPES = [
        ("task_01", "Quick Task"),
        ("task_02", "Medium Task"),
        ("task_03", "Long Task"),
        ("task_04", "Very Long Task"),
        ("task_05", "Extremely Long Task"),
    ]

    name = models.CharField(max_length=50, choices=TASK_TYPES, unique=True)
    execution_time_multiplier = models.FloatField()  # Time multiplier in seconds


class JobQueue(models.Model):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_time = models.FloatField(null=True, blank=True)
    worker_type = models.CharField(max_length=20, null=True, blank=True)



    def calculate_estimated_time(self):
        # Assuming the job has a time multiplier (task time per record)
        task_time_per_record = self.job.execution_time_multiplier
        # record_count = self.site.userrecords_set.count()  # Assuming there's a related set for UserRecords
        record_count = RECORD_MAP[self.site.record_capicity]        
        # Calculate estimated time
        self.estimated_time = record_count * task_time_per_record
        return self.estimated_time
    
    def classify_worker(self):
        if self.estimated_time <= 200:
            self.worker_type = 'worker_1'  # Very Fast
        elif 200 < self.estimated_time <= 1000:
            self.worker_type = 'worker_1'  # Fast
        elif 1000 < self.estimated_time <= 2000:
            self.worker_type = 'worker_2'  # Medium
        elif 2000 < self.estimated_time <= 10000:
            self.worker_type = 'worker_2'  # Slow
        elif 10000 < self.estimated_time <= 2000000:
            self.worker_type = 'worker_3'  # Very Slow
        else:
            self.worker_type = 'worker_1'  # Default worker
        return self.worker_type
