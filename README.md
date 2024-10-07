# Superheroes

## Introduction

The Superhero API is a Flask-based web application that manages information about superheroes and their superpowers. It provides a RESTful API for creating, reading, updating, and deleting data about heroes, powers, and the associations between them.

## Features

- List all superheroes
- Retrieve details of a specific superhero, including their powers
- List all superpowers
- Retrieve details of a specific superpower
- Update superpower descriptions
- Create associations between heroes and powers (HeroPower)

## Technologies Used

- Python 3.8+
- Flask: Web framework
- Flask-SQLAlchemy: ORM for database operations
- SQLite: Database

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/superhero-api.git
   cd superhero-api
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   flask db init
   flask db migrate -m 'Initial Migration'
   flask db upgrade head
   ```

5. Run the application:
   ```
   flask run
   ```

The API will be available at `http://localhost:5555`.

## Database Schema

The application uses three main models:

1. Hero:
   - id: Integer, primary key
   - name: String, hero's real name
   - super_name: String, hero's superhero name

2. Power:
   - id: Integer, primary key
   - name: String, name of the superpower
   - description: String, description of the superpower

3. HeroPower:
   - id: Integer, primary key
   - strength: String, strength level of the power for this hero
   - hero_id: Integer, foreign key to Hero
   - power_id: Integer, foreign key to Power

## API Endpoints

1. GET /heroes
   - Returns a list of all heroes

2. GET /heroes/:id
   - Returns details of a specific hero, including their powers

3. GET /powers
   - Returns a list of all superpowers

4. GET /powers/:id
   - Returns details of a specific superpower

5. PATCH /powers/:id
   - Updates the description of a superpower

6. POST /hero_powers
   - Creates a new association between a hero and a power

For detailed information on request/response formats, please refer to the API documentation.

## Error Handling

The API uses conventional HTTP response codes to indicate the success or failure of requests. In general:

- 2xx codes indicate success
- 4xx codes indicate an error that failed given the information provided
- 5xx codes indicate an error with the server

Common error codes:
- 400: Bad Request - Missing required fields
- 404: Not Found - Resource not found
- 422: Unprocessable Entity - Validation errors

## Testing

You can test the API using tools like Postman or curl. Here are some example requests:

1. Get all heroes:
   ```
   GET http://localhost:5555/heroes
   ```

2. Create a new HeroPower:
   ```
   POST http://localhost:5555/hero_powers
   Content-Type: application/json

   {
     "strength": "Average",
     "power_id": 1,
     "hero_id": 3
   }
   ```

For more detailed testing instructions, please refer to the testing documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
