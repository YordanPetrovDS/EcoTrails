# REST API EcoTrails

This API is a backend of a site for Ecotrails. The user can share his journeys, edit them and also search for new trips.

## Install

```
pip install -r requirements.txt
```

## Run the app in Powershell:

```
venv/Scripts/Activate.ps1
$env:FLASK_APP = "main.py"
$env:FLASK_ENV = "development"
flask run
```

## Run the tests in Powershell

```
pytest tests
```

# REST API

The REST API to the example app is described below.

## Get list of Things

### Request

`GET /ecotrails`

```
curl -i -H 'Accept: application/json' http://localhost:5432/ecotrails
```

### Response

```
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json
Content-Length: 2

[]
```
