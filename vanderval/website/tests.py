from website.models import Site, Job, UserRecords
from faker import Faker
import random
import uuid

fake = Faker()

# Function to create jobs
def create_job(name, execution_time_multiplier):
    job, created = Job.objects.get_or_create(
        name=name,
        defaults={"execution_time_multiplier": execution_time_multiplier},
    )
    if created:
        print(f"Created job {name}")
    else:
        print(f"Job {name} already exists")

# Create Jobs if not already created
create_job("task_01", 0.001)
create_job("task_02", 0.01)
create_job("task_03", 0.1)
create_job("task_04", 1)
create_job("task_05", 10)

# Function to create sites if the URL is unique
def create_site(name, domain, url, description, record_capicity):
    site, created = Site.objects.get_or_create(
        url=url,  # Ensure that the URL is unique
        defaults={
            "name": name,
            "domain": domain,
            "description": description,
            "record_capicity": record_capicity,
        }
    )
    if created:
        print(f"Created site {name} with URL {url}")
    else:
        print(f"Site with URL {url} already exists")

# Add Sites with different record capacities
create_site("Customer A", "a.com", "http://a.com", "Customer A", 3)  # High capacity
create_site("Customer B", "b.com", "http://b.com", "Customer B", 2)  # Medium capacity
create_site("Customer C", "c.com", "http://c.com", "Customer C", 1)  # Low capacity

# Function to create users based on site record capacity
def create_users_for_site(site):
    if site.record_capicity == 1:  # Low capacity
        num_users = random.randint(10, 100)
    elif site.record_capicity == 2:  # Medium capacity
        num_users = random.randint(100, 500)
    elif site.record_capicity == 3:  # High capacity
        num_users = random.randint(500, 1000)
    else:
        num_users = 0

    print(f"Creating {num_users} users for {site.name} ({site.get_record_capicity_display()})")
    
    # Create the users with unique emails by appending a UUID
    for _ in range(num_users):
        email = f"{fake.unique.email().split('@')[0]}+{str(uuid.uuid4())[:8]}@{fake.domain_name()}"
        
        UserRecords.objects.create(
            site=site,
            name=fake.name(),
            email=email,  # Unique email with appended UUID
            phone=fake.phone_number(),
            address=fake.address(),
            country=fake.country(),
            state=fake.state(),
            city=fake.city(),
            pincode=fake.zipcode(),
            dob=fake.date_of_birth(),
            is_active=True
        )

# Create users for Site A (High capacity)
create_users_for_site(Site.objects.get(url="http://a.com"))

# Create users for Site B (Medium capacity)
create_users_for_site(Site.objects.get(url="http://b.com"))

# Create users for Site C (Low capacity)
create_users_for_site(Site.objects.get(url="http://c.com"))
