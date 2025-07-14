# Rachunki

Rachunki is a Python application for managing user taxes, subscriptions, income and payments.

## Features (not yet implemented)

- Create and manage user accounts
- Track your subscriptions
- Check tax payment statuses
- Make tax payments
- View and edit payment details

## Table of content
1. [Installation](#Installation)
2. [Documentation](#Documentation)
3. [Contributing](#Contributing)

## Installation

This project is run with docker compose, but can be used without it too.
For it to work without docker compose, be sure to have POSTGRESQL.

#### Steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/Vronst/PayTrack.git
    cd PayTrack
    ```
    **(For implementing frontend)**
    Or install project with with uv or something similar:
    ```sh 
    uv add https://github.com/Vronst/PayTrack.git
    ```
    and skip later steps.

2. Create venv and install dependencies.
    *I'm working with uv, so this step should be alternated if uv is not used.*
    ```sh
    uv sync
    ```

4. Set up the environment variables in the [.env]() file:
    ```env
    DB_USER='your_postgres_user'
    DB_PASSWORD='your_postgres_password'
    HOST='localhost'
    PORT='5432'
    DATABASE ='your_database_name'
    ```

## Usage

For now there is no functionality yet, just models, schemas and tests. 
To run tests in docker run:
    ```sh
    docker compose up --build -d 
    docker exec paytrack uv run pytest
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
I will only cover backend part of this project, frontend desing will be done by UI/UX designer,
while frontend code will not be touched, only API will be created to allow for later development of it.
Feel free to create your own frontend for this project to your portfolio!

## License

This project is licensed under the MIT License.

## Documentation

Full documentation [link](https://vronst.github.io/PayTrack/)
