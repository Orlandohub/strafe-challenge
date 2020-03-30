# Strafe

<p>Docker microservises for Database and App api's</p>

## Run project

```bash
docker-compose up -d --build
```

## Run Tests

```bash
docker-compose exec database python manage.py test
docker-compose exec app python manage.py test
```

## App Endpoints

**Get match by ID**: ```http://127.0.0.1:5003/get-match/<id>```
**Get matches by date**: ```http://127.0.0.1:5003/get-match/<mm-dd-yyyy>```
**Get all available matches**: ```http://127.0.0.1:5003/all-matches```

## Database Endpoints

**Get all available matches**: ```http://127.0.0.1:5002/all-matches```

**Sign up Admin**:

```
http://127.0.0.1:5002/auth/signup
payload={ username: <username>, password: <password>}
```

**Log in Admin**:

```
http://127.0.0.1:5002/auth/signup
payload={ username: <username>, password: <password>}
response=<token>
```

**Add new match (Token Required)**:

```
http://127.0.0.1:5002/add-match
payload={
  players = []
  state = string
  start_date_time = mm-dd-yyyy
  end_date_time = mm-dd-yyyy
  score = integer
}
```

Ex.:
```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"start_date_time":"07/07/2020"}' http://127.0.0.1:5002/add-match
```

**Update existing match (Token Required)**:

```
http://127.0.0.1:5002/update-match/<id>
payload={
  players = []
  state = string
  start_date_time = mm-dd-yyyy
  end_date_time = mm-dd-yyyy
  score = integer
}
```

Ex.:
```bash
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"score":2500}' http://127.0.0.1:5002/update-match/250
```
