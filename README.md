# Crud Application
Medicine Database API
This Flask application provides a RESTful API for managing medicines in a database. It allows users to sign up, sign in, view all medicines, create new medicines, update existing medicines, and delete medicines.

## API Endpoints
The API provides the following endpoints:

- Signup (POST /signup): Creates a new user in the database. <br/>
Request body format:
```
{
  "username": "string",
  "password": "string",
  "role": "string" (optional, defaults to "user")
}
```

- Signin (POST /signin): Authenticates a user and returns a success message. <br/>
  Request body format: 
```
{
  "username": "string",
  "password": "string"
}
```

- Get All Medicines (GET /medicines): Retrieves a list of all medicines in the database. <br/>
Response format:
```
[
  {
    "id": integer,
    "title": "string",
    "company": "string"
  },
  ...
]
```

- Create Medicine (POST /medicine): Creates a new medicine in the database. <br/>
Request body format:

```
{
  "title": "string",
  "company": "string" (optional)
}
```


- Delete Medicine (DELETE /medicine/<int:id>): Deletes a medicine with the specified ID.

- Update Medicine (PUT /medicine/<int:id>): Updates an existing medicine with the specified ID. <br/>
  Request body format:

```
{
  "title": "string" (optional),
  "company": "string" (optional)
}
```

### Running the Application
Start the development server:
```
python app.py
```

This will run the Flask application on http://127.0.0.1:5000/ (default port) by default.

