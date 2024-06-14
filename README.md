# Telegram Bot

This is a Telegram bot implemented using the `aiogram` library. The bot provides various functionalities including fetching cryptocurrency prices, filtering forbidden words, managing user warnings and restrictions, and several administrative commands.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Commands](#commands)
- [Forbidden Words](#forbidden-words)
- [Contributing](#contributing)
- [License](#license)

## Features
- Fetch cryptocurrency prices from the CoinGecko API
- Filter forbidden words and phrases
- Warn and restrict users for violations
- Admin commands: mute, unmute, ban, unban, pin, unpin, delete messages
- Welcome new chat members
- Report messages to admins
- Customizable forbidden words list

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Eskotik/Tg-moderator.git
    cd Tg-moderator
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project directory and add your environment variables (see [Environment Variables](#environment-variables)).

4. Run the bot:
    ```sh
    python main.py
    ```

## Usage
1. Start the bot and add it to your Telegram group or supergroup.
2. Use the commands listed below to interact with the bot.

## Environment Variables
The bot requires several environment variables. Create a `.env` file in the root of your project and add the following variables:
- `ADMIN_ID=<your_admin_id>`
- `BOT_TOKEN=<your_bot_token>`
- `EXEMPT_CHANNEL_ID=<your_exempt_channel_id>`
- `WHITE_CHANNEL_ID=<your_white_channel_id>`

## Commands
### User Commands
- `/p <coin>` - Get the current price, market cap, and 24-hour volume of a cryptocurrency. Example: `/p bitcoin`
- `/me` - Get information about the user.
- `/report` - Report a message to admins.

### Admin Commands
- `!ban` - Ban a user.
- `!unban` - Unban a user.
- `!mute <duration>` - Mute a user for a specified duration. Examples: `!mute 15m`, `!mute 1h`
- `!unmute` - Unmute a user.
- `!pin` - Pin a message.
- `!unpin` - Unpin a message.
- `!del` - Delete a message.

### Fun Commands
- `/dont_click_me` - Randomly mute the user who sent the command for 1 to 10 minutes.

## Forbidden Words
You can customize the list of forbidden words and phrases by editing the `forbidden_words.json` file. The bot will check for these words in messages and take appropriate action if they are found.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.
