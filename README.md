# Michaelangelo-AI
This project was made for the AI challenge in ADA School.
This README file will guide you step-by-step through how to set up the code and use it properly. This is a text-based tutorial. A video based tutorial is also uploaded in the repository.

0) Requirements
- PyCharm or Visual Studio Code (I personally recommend PyCharm)
- Telegram
- DB browser for SQLite

1) Setting up the Telegram Bot.
   
First of all, you must create a bot in telegram. For this, you should use BotFather. You can use the link below to access it:
https://t.me/BotFather
Once you open it, type the command "/newbot". Write its name (Michaelangelo), give it a username, and once you do, BotFather will provide you with your BOT TOKEN. Copy paste this in the designated location within the provided code. DO NOT SHARE THIS TOKEN. If you want to customize your bot a little more, use the "/mybots" command and edit whatever you wish. Customization isn't necessary for the code to work (except Edit Commands section), but the options I used are provided below:

Description:
Michaelangelo is an artist that can make your wildest dreams into a piece of art! An AI image generator prepared for anything.

About:
AI image generator

Botpic:

![telegram-cloud-photo-size-2-5438480078200761727-x](https://github.com/user-attachments/assets/f4f415ad-cf2c-46e1-a176-f0689eac21a1)

Use the "/mybots" command, then press "Edit Commands". If you do not do this, the command codes in the script will not work. It is self explanatory, and you can do anything with it, but for this script, copy paste the text below:

start - Find out what the bot can do.

help - Get assistance for this bot. 

generate - give a prompt to generate an image

Once that is done, you can type the name of your bot in the user search bar and it will pop up. If you start the chat, nothing will happen if the code is not connected. To connect the script to telegram, as mentioned before, you must copy paste your API key into the script.

2) Setting up HuggingFace.
   
Enter "https://huggingface.co/". Once you do so, you should either Log In or Sign Up if you haven't yet. At the top right is your profile icon. Press it, and you will see an "Access Tokens" option. That is where you create your API key. Press on "+Create new token". It might seem confusing since most models don't ask for permissions like Hugging Face does. Just keep the Finegrained option (which is default), and enable all permissions. After that, it will show your API key. BEWARE: Your HuggingFace API key will only be shown ONE TIME. Copy paste it somewhere else to keep it safe. DO NOT SHARE THIS KEY.
When that's done, simply copy and paste your API key into the designated area within the script. This is how we will connect to Hugging Face's AI services.

4) Setting up the script.
   
As mentioned before, I personally recommend using PyCharm to set up the script, for the sake of comfort and easiness. It doesn't just end with copy pasting the script. You must paste your Bot and API tokens where they're required. After that, you will have to download a multitude of libraries. Copy paste the scripts given below into the terminal to download the required libraries.

![image](https://github.com/user-attachments/assets/573b84d4-ed61-428b-a790-9438bef23bb4)

pip install python-telegram-bot

pip install python-telegram-bot --upgrade (optional)

pip install requests

pip install huggingface_hub

Once this is done, your code should operate properly. Press the Run button, and it should show "Bot is running...". There might be an error like this:

"/Users/nmuradli/PycharmProjects/Michaelangelo/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn("
  
Don't mind it. It will not stop your code, nor will it interrupt any process. You can ignore it. Generally, most common errors, generation attempts and requests should show up in an easy-to-read way while the code is running. The most common one is "Model is busy or failed after several attempts". This indicates that Stable Diffusion servers are too busy and requests to HuggingFace were not returned. Don't worry, it's not a fault in the code! Try again after waiting a little bit and it should work.

4) Testing
   
Once the bot is running, go back to telegram and test out all the commands, generations, typing animation and prompts. Everything worked for me, but if you have an issue, you can contact me, research online, or easiest of all- ask ChatGPT, a fellow AI model!



