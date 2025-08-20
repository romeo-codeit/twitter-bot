# Twitter Bot

This is a Twitter bot that automatically posts unique, engaging content multiple times per day.

## Features

- Posts automatically multiple times per day.
- Each post is unique.
- Content is focused on the tech niche.
- Mix of short tweets and tweet threads.
- Auto-generates or fetches relevant images.
- 100% free to run.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    -   Create a `.env` file in the root of the project.
    -   Copy the contents of `.env.example` into `.env`.
    -   Fill in the values for the environment variables:
        -   `TWITTER_API_KEY`: Your Twitter API key.
        -   `TWITTER_API_SECRET_KEY`: Your Twitter API secret key.
        -   `TWITTER_ACCESS_TOKEN`: Your Twitter access token.
        -   `TWITTER_ACCESS_TOKEN_SECRET`: Your Twitter access token secret.
        -   `UNSPLASH_ACCESS_KEY`: Your Unsplash API key.

4.  **Run the bot:**
    ```bash
    python main.py
    ```

## How to get the API keys

### Twitter

1.  Apply for a Twitter Developer account [here](https://developer.twitter.com/).
2.  Create a new project and an app.
3.  Generate your API key, API secret key, access token, and access token secret.

### Unsplash

1.  Create an account on [Unsplash](https://unsplash.com/).
2.  Go to your applications page and create a new application.
3.  Your API key will be available on the application page.
