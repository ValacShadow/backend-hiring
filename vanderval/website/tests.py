from website.models import Site, Job, UserRecords

# # Add Sites
# Site.objects.create(name="Customer A", domain="a.com", url="http://a.com", description="Customer A", record_capicity=1)
# Site.objects.create(name="Customer B", domain="b.com", url="http://b.com", description="Customer B", record_capicity=2)

# # Add Jobs
# Job.objects.create(name="task_01", execution_time_multiplier=0.001)
# Job.objects.create(name="task_02", execution_time_multiplier=0.01)
# Job.objects.create(name="task_03", execution_time_multiplier=0.1)
# Job.objects.create(name="task_04", execution_time_multiplier=1)
# Job.objects.create(name="task_05", execution_time_multiplier=10)

 # Add Sites
site_a = Site.objects.create(name="Customer A", domain="a.com", url="http://a.com", description="Customer A", record_capicity=3)
site_b = Site.objects.create(name="Customer B", domain="b.com", url="http://b.com", description="Customer B", record_capicity=2)
site_c = Site.objects.create(name="Customer C", domain="c.com", url="http://c.com", description="Customer C", record_capicity=1)

# Add Users for Site A
UserRecords.objects.create(site=site_a, name="John Doe", email="john.doe@a.com", phone="1234567890", address="123 A Street", country="Country A", state="State A", city="City A", pincode="123456", dob="1980-01-01", is_active=True)
UserRecords.objects.create(site=site_a, name="Jane Smith", email="jane.smith@a.com", phone="1234567891", address="124 A Street", country="Country A", state="State A", city="City A", pincode="123457", dob="1990-02-01", is_active=True)

# Add Users for Site B
UserRecords.objects.create(site=site_b, name="Alice Green", email="alice.green@b.com", phone="9876543210", address="125 B Street", country="Country B", state="State B", city="City B", pincode="654321", dob="1985-05-15", is_active=True)
UserRecords.objects.create(site=site_b, name="Bob Brown", email="bob.brown@b.com", phone="9876543211", address="126 B Street", country="Country B", state="State B", city="City B", pincode="654322", dob="1995-03-25", is_active=True)

# Add Users for Site C
UserRecords.objects.create(site=site_c, name="Alice rt", email="alice.tr@b.com", phone="9876543270", address="125 B Street", country="Country B", state="State B", city="City B", pincode="654321", dob="1985-05-15", is_active=True)
UserRecords.objects.create(site=site_c, name="POP Brown", email="pop.brown@b.com", phone="9836543211", address="126 B Street", country="Country B", state="State B", city="City B", pincode="654322", dob="1995-03-25", is_active=True)
