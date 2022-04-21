# To run the app
This code follows the tutorial by Moses Maina
https://www.section.io/engineering-education/how-to-build-a-vue-app-with-flask-sqlite-backend-using-docker/

## Make sure your pipenv is activated and all necessary packages were installed
```
python -m pipenv shell
install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy flask-cors
```

## Possibley create the DB in interactive shell 
```
pipenv run python
>>> from app import db # import db
>>> db.create_all()
```

## Inside the folder flask-api: Start flask
```
export FLASK_API=app
flask run
```

# Within flask-frontend:Start the Vue Frontend

## Go into the frontend folder and setup the Project
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```
