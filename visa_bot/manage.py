import os
import sys
import multiprocessing


def run_django_server():
    """Run Django's development server."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visa_bot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(['manage.py', 'runserver'])


def run_telegram_bot():
    """Run the Telegram bot."""
    lock_file = "/tmp/telegram_bot.lock"

    if os.path.exists(lock_file):
        print("Bot is already running.")
        return

    # Create lock file
    with open(lock_file, "w") as f:
        f.write(str(os.getpid()))

    try:
        from bot.bot import application  # Import your bot's application
        print("Starting Telegram bot...")
        application.run_polling()
    finally:
        os.remove(lock_file)


def main():
    """Run both the Django server and the bot using multiprocessing."""
    django_process = multiprocessing.Process(target=run_django_server)
    django_process.start()

    bot_process = multiprocessing.Process(target=run_telegram_bot)
    bot_process.start()

    django_process.join()
    bot_process.join()


if __name__ == '__main__':
    main()
