# Clinic app

[![Coverage Status](https://coveralls.io/repos/github/hendelbah/clinic/badge.svg?branch=main)](https://coveralls.io/github/hendelbah/clinic?branch=main)
[![Build Status](https://app.travis-ci.com/hendelbah/clinic.svg?branch=main)](https://app.travis-ci.com/hendelbah/clinic)

### Web application for managing appointments in a clinic.

### [*See the app in the original repository*](https://github.com/hendelbah/clinic)

## With this app you can:

- **Display a list of doctors that work in the clinic**
- **Log in as an administrator or a doctor**
- **Display your profile and change password**
- **As an administrator:**
    - **Display a list of users**
    - **Display a list of doctors**
    - **Display a list of patients**
    - **Display a list of appointments and the total income from them**
    - **Change (add / edit / delete) the above data**
- **As a doctor:**
    - **Display a list of booked, unfilled and archived appointments, related to current doctor's account**
    - **Fill in info for successful (yet unfilled) appointments**

## How to build this project:

- #### Navigate to the project root folder
- #### Optionally set up and activate the virtual environment:
    ```
    virtualenv venv
    source venv/bin/activate
    ```
- #### Install the requirements:
    ```
    pip install -r requirements.txt
    ```
- #### Configure MySQL database
- #### Set the following environment variables<sup>*</sup>:
    - Flask app:
      ```
      FLASK_APP=clinic_app
      ```
    - Database:
      ```
      MYSQL_USER = <your_mysql_user>
      MYSQL_PASSWORD = <your_mysql_user_password>
      MYSQL_SERVER = <your_mysql_server>
      MYSQL_DATABASE = <your_mysql_database_name>
      ```
    - Optional:
      ```
      FLASK_SECRET_KEY = <your_secure_key>
      FLASK_CONFIG = [production|development]
      ```

  *<sup>\*</sup>You can set these in .env file in the application root directory as the project uses dotenv module to load
  environment variables(except `FLASK_APP` of course)*

- #### Run migrations to create database infrastructure:
    ```
    flask db upgrade
    ```
- #### Optionally populate the database with sample data
    ```
    python -m clinic_app.service.populate
    ```
- #### Run the project locally:
    ```
    python -m flask run
    ```
- #### Also, you can run project on gunicorn:
    ```
    gunicorn clinic_app:app
    ```

You can set gunicorn options in `gunicorn.conf.py` file in app's root directory.

## Now you should be able to access the web service and web application:

### Web Service (API):

```
localhost:5000/api/users?search_email=<str>
localhost:5000/api/users/<uuid>
localhost:5000/api/doctors?search_name=<str>&no_user=<1 or nothing>
localhost:5000/api/doctors/<uuid>
localhost:5000/api/patients?search_phone=<str>&search_name=<str>
localhost:5000/api/patients/<uuid>
localhost:5000/api/appointments?doctor_uuid=<str>&patient_uuid=<str>&doctor_name=<str>&patient_name=<str>&date_from=<YYYY-MM-DD>&date_to=<YYYY-MM-DD>
localhost:5000/api/appointments/<uuid>
localhost:5000/api/appointments/stats?<same filters as for appointments>
```

Also, all collection resources accept `page` and `per_page` GET parameters

#### Web Service endpoints are documented with Flasgger at:

```
localhost:5000/apidocs/
```

### Web Application:

#### After population, to log in you can use following email - password:

- ##### `root` - `root1234`: admin user
- ##### `doctor_001@spam.ua` - `doctor1234`: admin and doctor user

#### Routes:

```
localhost:5000/
localhost:5000/doctors

localhost:5000/login
localhost:5000/logout
localhost:5000/profile

localhost:5000/admin-panel/

localhost:5000/admin-panel/users
localhost:5000/admin-panel/users/new
localhost:5000/admin-panel/users/<uuid>
localhost:5000/admin-panel/users/<uuid>/delete

localhost:5000/admin-panel/doctors
localhost:5000/admin-panel/doctors/new
localhost:5000/admin-panel/doctors/<uuid>
localhost:5000/admin-panel/doctors/<uuid>/delete

localhost:5000/admin-panel/patients
localhost:5000/admin-panel/patients/new
localhost:5000/admin-panel/patients/<uuid>
localhost:5000/admin-panel/patients/<uuid>/delete

localhost:5000/admin-panel/appointments
localhost:5000/admin-panel/appointments/new
localhost:5000/admin-panel/appointments/<uuid>
localhost:5000/admin-panel/appointments/<uuid>/delete

localhost:5000/doctor-panel/
localhost:5000/doctor-panel/appointments/booked
localhost:5000/doctor-panel/appointments/unfilled
localhost:5000/doctor-panel/appointments/archived
localhost:5000/doctor-panel/appointments/<uuid>
```