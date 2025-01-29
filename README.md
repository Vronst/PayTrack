# Rachunki

Rachunki is a Python application for managing user taxes and payments. It allows users to create accounts, check their tax statuses, make payments, and view or edit payment details.

## Features

- Create and manage user accounts
- Check tax payment statuses
- Make tax payments
- View and edit payment details
- Log activities and errors

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/rachunki.git
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

4. Set up the environment variables in the [.env](http://_vscodecontentref_/15) file:
    ```env
    POSTGRES_USER='your_postgres_user'
    POSTGRES_PASSWORD='your_postgres_password'
    POSTGRES_HOST='localhost'
    POSTGRES_PORT='5432'
    POSTGRES_DB='your_database_name'
    LOGS_PATH='/path/to/logs/'
    ```

## Usage

1. Initialize the database:
    ```sh
    python -m app.database.engine
    ```

2. Run the application:
    ```sh
    python manage.py
    ```

## Logging

Logs are stored in the [logs](http://_vscodecontentref_/16) directory:
- [db.log](http://_vscodecontentref_/17): Logs related to database operations
- [logs.txt](http://_vscodecontentref_/18): General logs
- [taxes.log](http://_vscodecontentref_/19): Logs related to tax payments
- [user.log](http://_vscodecontentref_/20): Logs related to user activities

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.