# Google Calendar Integration

## After pulling the repository, follow the steps to run the code

###### 1. Create a folder and open terminal/command prompt in that folder.

###### 2. Create a virtual environment in the folder.
```
python -m venv env
```

###### 3. And activate the virtual environment.
```
.\env\Scripts\activate
```

###### 4. Install the dependencies.
```
pip install -r requirements.txt
```

###### 5. (not required, but to avoid warnings)
```
python manage.py makemigrations
```

###### 6. (not required, but to avoid warnings)
```
python manage.py migrate
```

###### 7. Add SECRET_KEY & DEBUG values to the .env file ,add BASE_URL ex: http://127.0.0.1:8000 and use the redirect url with the same BASE_URI in the google calendar API to get events list to that API endpoint after authorization.

###### 8. Finally, start the server and then go to BASE_URI+"rest/v1/calendar/init/".
```
python manage.py runserver
```