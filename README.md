# Coding Challenge
Coding challenge by PanOrbit.

  - Framework used Django(Python), Django REST framework
  - Database - Mysql


### Installation

Coding Challenge requires [python](https://www.python.org/) 3+ to run.

After making virtual enviroment...

```sh
$ pip install -r requirements.txt
```
Run world.sql in sql folder to mysql

Create .env like .env.example in the project folder with appropriate values

```sh
$ python manage.py migrate
```

### URLS

* /sign_up/ - For user registerartion
* /login/ - Login page
* /verify_otp/ - Verify OTP
* /logout/ - Logout
* / - Search Dashboard after login
* /country/[country_code]/ - detail of a country
* /api/sign_up/ - api for sign up
* /api/request_otp/ - api for requesting otp for login
* /api/otp_verfifcation/ - api for otp_verification(login)
* /api/logout/ - api for logout


