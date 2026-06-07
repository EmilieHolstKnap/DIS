# KU Event Hub

## Initialization ✔

### TA modification:

Run with Docker:
``` shell
docker-compose up -d
```

Clone / download the repository files and install the required packages (preferably inside a virtual environment):
    pip install -r requirements.txt

Create a PostgreSQL database (preferably named `ku_event_hub`).

If running locally, configure the following environment variables:
    export PGUSER=<postgres_username>
    export PGPASSWORD=<postgres_password>
    export PGDATABASE=ku_event_hub
    export PGHOST=127.0.0.1
    export PGPGPORT=5432

Then run the following command to initialize the database:

    python scripts/init_db.py

When the database has been initialized, start the application:

    flask run --debug

The application will be available at:
    http://127.0.0.1:5000

## Folder Setup 

The application is divided into several folders:

- controllers: Contains all Flask routes and request handling logic.
- models: Contains database queries and application logic.
- data: Contains the CSV datasets used to populate the event database.
- static: Contains CSS files and static images.
- templates: Contains all HTML templates rendered by Flask.

At the root folder of the project several files are present with the following roles:

- app.py: Initializes the Flask application and registers blueprints.
- database.py: Handles database connections and initialization.
- docker-compose.yml: Docker configuration for the PostgreSQL database and Flask application.
- pyproject.toml: Project dependencies and configuration.

## Routes 

The application consists of two main modules: authentication and event management.

### Authentication

- /login: Login and registration page.
- /logout: Logs out the current user.

### Events

- /: Home page.
- /event: Browse all available events.
- /events/<event_id>: View details for a specific event.
- /events/<event_id>/save: Save an event.
- /events/<event_id>/unsave: Remove a saved event.
- /my-events: View all saved events.

### Organizers

- /organizers: View organizers and their events.
- /organizers/<organizer>/subscribe: Subscribe to an organizer.
- /organizers/<organizer>/unsubscribe: Unsubscribe from an organizer.

## Database Structure 🗄️

The application uses PostgreSQL and contains the following tables:

- users: Registered users and password hashes.
- events: Event information.
- event_types: Event categories.
- saved_events: Stores events saved by users.
- organizer_subscriptions: Stores organizer subscriptions.

## Features ⭐

### User Accounts

Users can:

- Register an account.
- Login and logout.
- Maintain a personal list of saved events.

Passwords are securely stored using Werkzeug password hashing.

### Event Discovery

Users can:

- Browse upcoming events.
- Filter events by organizer.
- Filter events by event type.
- View detailed event information.

### Saved Events

Logged-in users can:

- Save events.
- Remove saved events.
- Access a personal "My Events" page.

### Organizer Subscriptions

Logged-in users can:

- Subscribe to organizers.
- Unsubscribe from organizers.
- Browse events grouped by organizer.

## Known Backend Issues / Intended Features ⁉

- Organizer subscriptions are currently stored and managed correctly, but subscribed organizers are not yet displayed on the "My Events" page.
- Organizer images currently rely on manually assigned image files rather than database-stored metadata.
- There is currently no administrative interface for adding or editing events through the application.
- Event recommendations based on user subscriptions have not yet been implemented.

Future improvements include displaying events from subscribed organizers directly on the user's personal page and implementing event notifications.

## Known Frontend Issues ☹

- Mobile responsiveness could be improved further, especially for event tables and navigation.
- Organizer pages currently use basic collapsible sections and could benefit from a richer visual layout.
- Event and organizer images are limited and currently require manual assignment.
- Success messages are not displayed after actions such as saving events, subscribing to organizers, or creating accounts.
- Missing favicon.ico console warning (ignored).
