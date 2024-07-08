
# Backend Stage 2 Task: User Authentication & Organisation

## Acceptance Criteria
Adhere to the following acceptance criteria for the task:

1. **Database Connection**
   - Connect your application to a Postgres database server.

2. **User Model**
   - Create a User model with the following properties:
     ```json
     {
       "userId": "string", // must be unique
       "firstName": "string", // must not be null
       "lastName": "string", // must not be null
       "email": "string", // must be unique and must not be null
       "password": "string", // must not be null
       "phone": "string"
     }
     ```
   - Ensure user id and email are unique.
   - Provide validation for all fields.
   - Return status code 422 with payload when there’s a validation error:
     ```json
     {
       "errors": [
         {
           "field": "string",
           "message": "string"
         }
       ]
     }
     ```

3. **User Authentication**
   - Implement user registration and login.
   - Hash the user’s password before storing them in the database.

## Endpoints

### User Registration
- **Endpoint:** `[POST] /auth/register`
- **Request Body:**
  ```json
  {
    "firstName": "string",
    "lastName": "string",
    "email": "string",
    "password": "string",
    "phone": "string"
  }
  ```
- **Successful Response:**
  ```json
  {
    "status": "success",
    "message": "Registration successful",
    "data": {
      "accessToken": "eyJh...",
      "user": {
        "userId": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "phone": "string"
      }
    }
  }
  ```
- **Unsuccessful Response:**
  ```json
  {
    "status": "Bad request",
    "message": "Registration unsuccessful",
    "statusCode": 400
  }
  ```

### User Login
- **Endpoint:** `[POST] /auth/login`
- **Request Body:**
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Successful Response:**
  ```json
  {
    "status": "success",
    "message": "Login successful",
    "data": {
      "accessToken": "eyJh...",
      "user": {
        "userId": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "phone": "string"
      }
    }
  }
  ```
- **Unsuccessful Response:**
  ```json
  {
    "status": "Bad request",
    "message": "Authentication failed",
    "statusCode": 401
  }
  ```

### Get User Record
- **Endpoint:** `[GET] /api/users/:id`
- **Response:**
  ```json
  {
    "status": "success",
    "message": "<message>",
    "data": {
      "userId": "string",
      "firstName": "string",
      "lastName": "string",
      "email": "string",
      "phone": "string"
    }
  }
  ```

### Get Organisations
- **Endpoint:** `[GET] /api/organisations`
- **Response:**
  ```json
  {
    "status": "success",
    "message": "<message>",
    "data": {
      "organisations": [
        {
          "orgId": "string",
          "name": "string",
          "description": "string"
        }
      ]
    }
  }
  ```

### Get Single Organisation
- **Endpoint:** `[GET] /api/organisations/:orgId`
- **Response:**
  ```json
  {
    "status": "success",
    "message": "<message>",
    "data": {
      "orgId": "string",
      "name": "string",
      "description": "string"
    }
  }
  ```

### Create Organisation
- **Endpoint:** `[POST] /api/organisations`
- **Request Body:**
  ```json
  {
    "name": "string", // Required and cannot be null
    "description": "string"
  }
  ```
- **Successful Response:**
  ```json
  {
    "status": "success",
    "message": "Organisation created successfully",
    "data": {
      "orgId": "string",
      "name": "string",
      "description": "string"
    }
  }
  ```
- **Unsuccessful Response:**
  ```json
  {
    "status": "Bad Request",
    "message": "Client error",
    "statusCode": 400
  }
  ```

### Add User to Organisation
- **Endpoint:** `[POST] /api/organisations/:orgId/users`
- **Request Body:**
  ```json
  {
    "userId": "string"
  }
  ```
- **Successful Response:**
  ```json
  {
    "status": "success",
    "message": "User added to organisation successfully"
  }
  ```

## Unit Testing
- Write appropriate unit tests to cover:
  - Token generation: Ensure token expires at the correct time and correct user details are found in the token.
  - Organisation: Ensure users can’t see data from organisations they don’t have access to.

## End-to-End Test Requirements for the Register Endpoint
- **Directory Structure:**
  - The test file should be named `auth.spec.ext` (ext is the file extension of your chosen language) inside a folder named `tests`. For example, `tests/auth.spec.ts` assuming using Typescript.
- **Test Scenarios:**
  1. **It Should Register User Successfully with Default Organisation:**
     - Ensure a user is registered successfully when no organisation details are provided.
     - Verify the default organisation name is correctly generated (e.g., "John's Organisation" for a user with the first name "John").
     - Check that the response contains the expected user details and access token.
  2. **It Should Log the User in Successfully:**
     - Ensure a user is logged in successfully when a valid credential is provided and fails otherwise.
     - Check that the response contains the expected user details and access token.
  3. **It Should Fail If Required Fields Are Missing:**
     - Test cases for each required field (firstName, lastName, email, password) missing.
     - Verify the response contains a status code of 422 and appropriate error messages.
  4. **It Should Fail if there’s Duplicate Email or UserID:**
     - Attempt to register two users with the same email.
     - Verify the response contains a status code of 422 and appropriate error messages.