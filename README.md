# Rachunki

Rachunki is a Python application for managing user taxes and payments. It allows users to create accounts, check their tax statuses, make payments, and view or edit payment details.

## Features

- Create and manage user accounts
- Check tax payment statuses
- Make tax payments
- View and edit payment details
- Log activities and errors

## Table of content
1. [Installation](#Installation)
2. [Logging](#Logging)
3. [Documentation](#Documentation)

## Installation

This project uses PostgreSQL, be sure you have it installed.

1. Clone the repository:
    ```sh
    git clone https://github.com/Vronst/PayTrack.git
    cd rachunki
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables in the [.env]() file:
    ```env
    POSTGRES_USER='your_postgres_user'
    POSTGRES_PASSWORD='your_postgres_password'
    POSTGRES_HOST='localhost'
    POSTGRES_PORT='5432'
    DataBase='your_database_name'
    LOGS_PATH='/path/to/logs/'
    ```

## Usage

Run the application in text mode:
    ```sh
    python manage.py -t
    ```

## Logging

Logs are stored in the [logs](http://_vscodecontentref_/4) directory:
- [db.log](): Logs related to database operations
- [logs.txt](): General logs
- [taxes.log](): Logs related to tax payments
- [user.log](): Logs related to user activities

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Documentation

Full documentation [link](https://vronst.github.io/PayTrack/)
