# This is the main entry point for the Twitter bot.
from scheduler import run_scheduler
from dotenv import load_dotenv

def main():
    """
    Main function to start the bot.
    """
    # Load environment variables from .env file
    load_dotenv()

    print("Starting Twitter bot...")
    run_scheduler()

if __name__ == "__main__":
    main()
