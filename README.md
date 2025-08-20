# Swifter - The Smart Twitter/X Automation Tool

Swifter is a full-stack web application that helps you automate your Twitter/X presence. It features a beautiful, modern dashboard where you can connect your Twitter account, manage a queue of content, set a custom posting schedule, and more.

This project is designed to be easy to set up and run using Docker.

## Quick Start (Docker)

Get up and running in 3 simple steps:

1.  **Set up your environment file.**
    - In the `backend` folder, copy `.env.example` to a new file named `.env`.
    - Open `.env` and add your secret keys. You can generate a `FERNET_KEY` with:
      ```bash
      python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
      ```

2.  **Build and run the app.**
    - From the project's root directory, run:
      ```bash
      docker-compose up --build
      ```

3.  **Log in and start tweeting!**
    - Open your browser to `http://localhost:3000`.
    - Create an account, log in, and connect your Twitter account in the dashboard.

---

## Features

-   **User Authentication**: Secure login and registration.
-   **Modern Dashboard**: A clean, beautiful UI to manage your bot's settings.
-   **Secure Twitter/X Integration**: Connect your Twitter API keys, which are stored securely using strong encryption.
-   **Content Queues**: A full CRUD interface for the content you want the bot to post.
-   **Flexible Scheduling**: An easy-to-use interface to set multiple posting times per day.
-   **Persistent & Dynamic Scheduling**: Uses APScheduler with a database backend to ensure your scheduled jobs are not lost on restart.

## Manual Local Setup (Without Docker)

If you prefer not to use Docker, you can run the application manually.

### Prerequisites

-   Node.js and npm
-   Python 3.11+ and pip

### Setup

1.  **Clone the repository and set up the `.env` file** as described in step 1 of the Quick Start guide.

2.  **Backend Setup:**
    -   `cd backend`
    -   `pip install -r requirements.txt`
    -   `python -m flask init-db` (Note: This requires `FLASK_APP=backend` to be set as an environment variable or for you to use a `.flaskenv` file).
    -   `python -m flask run --port 5001`

3.  **Frontend Setup:**
    -   `cd frontend`
    -   `npm install`
    -   `npm run dev`
    -   The frontend will be available at the address provided by Vite (usually `http://localhost:5173`).
