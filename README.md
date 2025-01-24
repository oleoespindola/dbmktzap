# MKTZAP API Integration

This repository contains a Python application that integrates with the MKTZAP API to fetch and update data in a MySQL database.

## Features
Fetches users, sectors, status, messages, and history from the MKTZAP API
Updates the mariadb database with the fetched data
Handles errors and exceptions using Telegram notifications

## Requirements
- Python 3.x
- requests library
- pandas library
- sqlalchemy library
- mysql-connector library
- telegram library

## Environment variables:
- telegram_token
- chat_id
- clientKey
- host
- port
- user
- password

## Setup
1. Clone the repository
2. Install the required libraries using pip install -r requirements.txt
3. Set the environment variables
4. Run the application using python app.py

## Usage
The application is designed to run automatically, fetching and updating data in the MySQL database. You can also run individual functions manually using the app.py script.

## Telegram Notifications
The application uses Telegram notifications to handle errors and exceptions. You can configure the Telegram token and chat ID in the telegram.py script.

## Database Schema
The MySQL database schema is not included in this repository. You will need to create the necessary tables and relationships to store the fetched data.

## API Documentation
The MKTZAP API documentation is not included in this repository. You can find the API documentation on the MKTZAP website.

## Contributing
Contributions are welcome! Please submit a pull request with your changes.

### License
This repository is licensed under the MIT License. See the LICENSE file for details.