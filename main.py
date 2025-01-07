import base64 #Used for turning JSON objects into images
import sqlite3 #Used to create reliable database
import time #Used for anything related to time
import requests
import random
#The ones below are everything we need to write this telegram bot code
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot token and Hugging Face API key
BOT_TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token
HUGGINGFACE_API_KEY = "YOUR_HUGGINGFACE_API_KEY"  # Replace with your Hugging Face API key

# Function to initialize the database for storing user info
def initialize_database():
    conn = sqlite3.connect("users.db")  # Connect to the SQLite database (creates if doesn't exist)
    cursor = conn.cursor()  # Cursor to execute SQL commands
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            telegram_id INTEGER UNIQUE
        )
    """)  # Create a table to store user information (ID, username, telegram ID) if it doesn't exist already
    conn.commit()  # Commit changes to the database
    conn.close()  # Close the connection to the database


# Function to add a user to the database
def add_user_to_database(username, telegram_id):
    conn = sqlite3.connect("users.db")  # Connect to the database
    cursor = conn.cursor()  # Create cursor object
    try:
        # Insert new user information (username, telegram_id) into the users table, ignore if user already exists
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, telegram_id)
            VALUES (?, ?)
        """, (username, telegram_id))
        conn.commit()  # Commit the changes to the database
    except Exception as e:
        print(f"Database error: {e}")  # Print any database errors
    finally:
        conn.close()  # Always close the connection


# Image generation, function to retry generating the image if model loading fails and some error handling
def generate_image_with_polling(url, headers, data, retries=3, delay=5):
    for attempt in range(retries):
        response = requests.post(url, headers=headers, json=data)  # Make POST request to the Hugging Face API

        print(f"Response status code: {response.status_code}")  # Debugging: Print the response status code

        if response.status_code == 200:
            # If the response contains an image in the headers, return the image content
            if "image" in response.headers.get("Content-Type", ""):
                return response.content
            try:
                # Try parsing JSON response and return the base64-decoded image if found
                response_json = response.json()
                if "data" in response_json and isinstance(response_json["data"], str):
                    return base64.b64decode(response_json["data"])
            except ValueError:
                return {"error": "Unexpected response format."}  # Error in parsing the response

        elif response.status_code in [500, 503]:
            # If the server is unavailable (500 or 503 errors), retry after a delay
            print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
            time.sleep(delay)  # Wait before retrying
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            return {"error": response.text}  # Return error message if unexpected status code

    return {"error": "Model is still busy or failed after several attempts."}  # Return error after retrying several times


# Command handler functions

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username or "Unknown"  # Get the user's username
    telegram_id = update.effective_user.id  # Get the user's Telegram ID
    add_user_to_database(username, telegram_id)  # Add the user to the database

    # Simulate typing animation
    await update.message.chat.send_action('typing')  # Start typing animation
    time.sleep(0.5)  # Wait for 0.5 seconds to simulate thinking time
    await update.message.reply_text("Greetings, traveller! My name is Michaelangelo, a renowned artist, unmatched on the field!")  # Send greeting message


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.chat.send_action('typing')  # Simulate typing animation
    time.sleep(0.5)  # Wait for a brief moment before sending a message
    await update.message.reply_text(
        "Here's what I can do for you:\n"
        "/start - An introduction, again.\n"
        "/help - Well, what I'm doing right now, of course!\n"
        "/generate - Paint a picture, just for you!"
    )  # Help message explaining bot commands


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.chat.send_action('typing')  # Simulate typing animation
    time.sleep(0.5)  # Wait before sending the message
    await update.message.reply_text("What shall I draw for thou, youngin?")  # Prompt user for the image prompt
    context.user_data['awaiting_prompt'] = True  # Set flag to await user's input


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = context.user_data  # Access user data to track conversation state

    # If the bot is awaiting the prompt for image generation
    if user_data.get('awaiting_prompt'):
        await update.message.chat.send_action('typing')  # Simulate typing animation
        time.sleep(0.5)  # Wait before processing input
        user_data['prompt'] = update.message.text  # Store the prompt text from the user
        user_data['awaiting_prompt'] = False  # Stop awaiting prompt
        user_data['awaiting_count'] = True  # Start awaiting the number of images

        # Ask the user how many images they want (max 5)
        await update.message.reply_text(
            "Perhaps you would like different versions! If so, how many? (Max: 5)"
        )
    # If the bot is awaiting the number of images to generate
    elif user_data.get('awaiting_count'):
        try:
            count = int(update.message.text)  # Try to convert the user's input to an integer
            if 1 <= count <= 5:
                await update.message.chat.send_action('typing')  # Simulate typing animation
                time.sleep(0.5)  # Wait for a brief moment before proceeding
                user_data['awaiting_count'] = False  # Stop awaiting count
                prompt = user_data['prompt']  # Get the previously stored prompt
                await update.message.reply_text(f"Painting {count} art piece(s) for: {prompt}")  # Notify user about how many pieces will be generated

                # Prepare for API call to generate the images
                url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2" #SD2 model webhook
                headers = {
                    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",  # Authorization with API key
                    "Content-Type": "application/json"
                }

                # Generate images based on the user's input count
                for i in range(count):
                    unique_prompt = f"{prompt} | Variation {random.randint(1, 10000)}"  # Add variation to the prompt
                    data = {"inputs": unique_prompt}  # Prepare the data for the API

                    await update.message.chat.send_action('typing')  # Simulate typing animation while generating
                    time.sleep(0.5)  # Simulate thinking time
                    response = generate_image_with_polling(url, headers, data)  # Call the function to generate image

                    if isinstance(response, bytes):  # If the response is an image (bytes)
                        image_path = f"generated_image_{i + 1}.png"  # Save image to file
                        with open(image_path, "wb") as f:
                            f.write(response)

                        with open(image_path, "rb") as f:
                            await update.message.reply_photo(photo=f, caption=f"Here is image {i + 1} for: {prompt}")  # Send the image to the user
                    elif isinstance(response, dict) and "error" in response:  # If an error occurred
                        await update.message.reply_text(f"Sorry, I couldn't draw that {i + 1}: {response['error']}")
                    else:
                        await update.message.reply_text(f"Unexpected response format for image {i + 1}. Try that again!")
            else:
                await update.message.chat.send_action('typing')  # Simulate typing animation
                time.sleep(0.5)  # Wait before replying
                await update.message.reply_text("Either 1 or 'till 5, my friend!")  # Inform the user to enter a valid number (1-5)
        except ValueError:
            await update.message.chat.send_action('typing')  # Simulate typing animation
            time.sleep(0.5)  # Wait for a brief moment
            await update.message.reply_text("Either too little or too much, youngin.")  # Handle non-integer input
    else:
        await update.message.chat.send_action('typing')  # Simulate typing animation
        time.sleep(0.5)  # Wait before sending the message
        await update.message.reply_text("I'm not here for chitchat, dear fellow! Use /help if you wish to familiarize yourself with my services.")  # Inform user to use commands in case they do anything else


# Main function to start the bot and connect handlers
def main():
    initialize_database()  # Initialize the database

    application = Application.builder().token(BOT_TOKEN).build()  # Create the bot application

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))  # /start command handler
    application.add_handler(CommandHandler("help", help_command))  # /help command handler
    application.add_handler(CommandHandler("generate", generate))  # /generate command handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Handle non-command messages

    print("Bot is running...")  # Inform that the bot is running in terminal
    application.run_polling()  # Start polling for new messages and commands


if __name__ == "__main__":
    main()  # Run the bot
