# What is this about?

there is a list of customers in the Site table. Each customer has a unique id and a name. Our servers are shared across all customers. Since resources are shared amongst all customers, we need to dynamically handle their asynchronous tasks. We need to create a system to handle the following tasks:

1. create a datastructure/store to store type of job based on their execution time. you can assume time in seconds and there are 5 types of jobs.
2. create a datastructure/store to store type of customer based on their record volume. large volume customers will tend to comsume more resources. you can assume there are 3 types of customers.
3. create relevant apis to support the interactions.
4. create workers which will pick up the job based on the customer type and job type and execute them. you can assume that each worker can execute only one job at a time.

refer website/models.py for Site Table <br>
refer website/tasks.py for the tasks to be executed

you can use any database, message queue, etc. to store the data. you can use any library to create the workers or any other part of the system. you can create any number of files, classes, functions, etc. to complete the assignment.

# Setup:

```
install python3.5, pip3 and venv
$ python3.5 -m venv almabase-venv
$ source almabase-venv/bin/activate
$ pip install --upgrade pip --trusted-host pypi.python.org
$ pip3 install -r requirements.txt
```

# How to submit the assignment:

1. Fork this repository
2. Create a new branch with your name
3. Commit your code to this branch
4. Create a pull request to this repository
5. Add your name and email to the README.md file

# What will be evaluated?

1. Code quality
2. high level design
3. api design

# Bonus:

create a deployment pipeline to deploy on a ubuntu VM. you can use any CI/CD tool for the same. <br>
or <br>
deploy on your own cloud provider and share the link with us.

# What next?

Once you have submitted the assignment, we will review your code and if it meets our requirements, we will get back to you within a week and schedule 1st round of interview. <br>
in the 1st round of interview, we will discuss the code and build few additional features.

### <i>Name</i>: Rajeev K L
### <i>Email</i>: rajeev@almabase.com
### <i>JD</i>: [Software Engineer](https://www.almabase.com/careers?ashby_jid=27df3851-fcea-47e2-af51-4c5aec17ff67)


## How to Run

### 1. Populate Data
First, populate the database with the required data by running the following command:
```bash
python manage.py test website

docker compose up


### Key Points:
- **Populate Data**: Running `python manage.py test website` will populate the database with necessary data, ensuring a smooth setup.
- **Run Server**: `docker compose up` starts the application and all necessary services.
- **API Endpoints**: You can use the provided API endpoints to interact with the application:
  - `submit/` allows submitting jobs.
  - `status/<job_id>/` lets you check the status of a specific job.

