import requests
import time
import json
import os
import asyncio
import telegram
from fake_useragent import UserAgent
import urllib3
from loguru import logger
import pyfiglet
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=''),
    format=(
        "<green>{time:DD/MM/YY HH:mm:ss}</green> | "
        "<level>{level:8} | {message}</level>"
    ),
    colorize=True
)

CONFIG_FILE = "config.json"
PROXY_FILE = "proxy.txt"

def read_config(filename=CONFIG_FILE):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"🔴 Error: {e}")
        exit(1)

def read_proxies(filename=PROXY_FILE):
    try:
        with open(filename, 'r') as file:
            proxies = file.readlines()
        return [proxy.strip() for proxy in proxies]
    except FileNotFoundError:
        logger.error(f"🔴 proxy.txt' file not found.")
        exit(1)

config = read_config()
bot_token = config.get("telegram_bot_token")
chat_id = config.get("telegram_chat_id")
appid = config.get("appid")

if not all([bot_token, chat_id, appid]):
    logger.error("Missing 'bot_token', 'chat_id', or 'appid' in 'config.json'.")
    exit(1)

bot = telegram.Bot(token=bot_token)
keepalive_url = "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive"
get_points_url = "https://www.aeropres.in/api/atom/v1/userreferral/getpoint"
extension_id = "fpdkjdnhkakefebpekbdhillbhonfjjp"
_v = "1.1.1"

ua = UserAgent()

def print_header():
    cn = pyfiglet.figlet_format("xDawnBot")
    print(cn)
    print("🌱 Season 1")
    print("🎨 by \033]8;;https://github.com/officialputuid\033\\officialputuid\033]8;;\033\\")
    print("✨ Credits: gilanx04")
    print('🎁 \033]8;;https://paypal.me/IPJAP\033\\Paypal.me/IPJAP\033]8;;\033\\ — \033]8;;https://trakteer.id/officialputuid\033\\Trakteer.id/officialputuid\033]8;;\033\\')

# Initialize the header
print_header()

def read_email_and_proxy():
    accounts = config.get("accounts", [])
    email_count = len([account for account in accounts if "email" in account])

    with open('proxy.txt', 'r') as file:
        proxy_count = sum(1 for line in file)

    return email_count, proxy_count

email_count, proxy_count = read_email_and_proxy()

print()
print(f"🔑 Emails: {email_count}.")
print(f"🌐 Loaded {proxy_count} proxies.")
print()

def get_user_input():
        user_input = ""
        while user_input not in ['yes', 'no']:
            user_input = input("🔵 Do you want to use proxy? (yes/no): ").strip().lower()
            if user_input not in ['yes', 'no']:
                print(f"🔴 Invalid input. Please enter 'yes' or 'no'.")
        return user_input == 'yes'

def read_accounts():
    return config.get("accounts", [])

def total_points(headers):
    try:
        response = requests.get(f"{get_points_url}?appid={appid}", headers=headers, verify=False)
        response.raise_for_status()
        json_response = response.json()
        
        if json_response.get("success") is False:
            logger.warning(f"Warning: {json_response.get('message', 'Error fetching points')}")
            return 0

        reward_data = json_response["data"]["rewardPoint"]
        referral_data = json_response["data"]["referralPoint"]

        return sum([reward_data.get("points", 0),
                    reward_data.get("registerpoints", 0),
                    reward_data.get("signinpoints", 0),
                    reward_data.get("twitter_x_id_points", 0),
                    reward_data.get("discordid_points", 0),
                    reward_data.get("telegramid_points", 0),
                    reward_data.get("bonus_points", 0),
                    referral_data.get("commission", 0)])
    except requests.exceptions.RequestException:
        logger.error(f"Error fetching points.")
        return 0

def keep_alive(headers, email, proxy=None, retries=3):
    payload = {
        "username": email,
        "extensionid": extension_id,
        "numberoftabs": 0,
        "_v": _v
    }
    headers["User-Agent"] = ua.random
    attempt = 0
    while attempt < retries:
        try:
            proxies = {"http": proxy, "https": proxy} if proxy else None
            response = requests.post(f"{keepalive_url}?appid={appid}", headers=headers, json=payload, verify=False, proxies=proxies)
            response.raise_for_status()
            json_response = response.json()
            if json_response.get("success", False):
                return True, "Keep alive successful."
            else:
                return False, json_response.get("message", "Keep alive failed.")
        except requests.exceptions.RequestException as e:
            attempt += 1
            logger.error(f"Attempt {attempt}/{retries} failed. Error: {str(e)[:30]}**")
            if attempt < retries:
                logger.info(f"Retrying...")
                time.sleep(3)  # Wait before retrying
            else:
                return False, "Error during keep alive after 3 attempts."
    return False, "Error during keep alive."

async def telegram_message(message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")

def countdown(seconds):
    logger.info(f"Restarting in: {seconds} seconds")
    time.sleep(seconds)

async def main():
    # Ask the user if they want to use proxies
    use_proxies = get_user_input()
    print(f"🔵 You selected: {'Yes' if use_proxies else 'No'}, ENJOY!\n")

    if use_proxies:
        proxies = read_proxies()
        proxy_idx = 0
    else:
        proxies = []
        proxy_idx = None  # No proxies used

    
    while True:
        accounts = read_accounts()
        if not accounts:
            break

        total_points_all_users = 0
        messages = ["📢 DAWN Internet Validator Extension\n"]

        for idx, account in enumerate(accounts):
            email = account["email"]
            token = account["token"]
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": ua.random
            }

            # Use proxy if available
            if proxy_idx is not None:
                proxy = proxies[proxy_idx % len(proxies)]
                parsed_proxy = urlparse(proxy)
                proxy_ip = parsed_proxy.hostname
                logger.info(f"📢 DAWN Validator - Account {idx + 1}")
                logger.info(f"📧 Email: {email}")
                logger.info(f"🌐 Using Proxy: {proxy_ip}")
            else:
                proxy = None
                logger.info(f"📢 DAWN Validator - Account {idx + 1}")
                logger.info(f"📧 Email: {email}")
                logger.info(f"🌐 Using No Proxy/Direct.")

            points = total_points(headers)
            total_points_all_users += points

            success, status_msg = keep_alive(headers, email, proxy)

            # If there is an error, try changing proxy
            if not success and proxies and proxy_idx is not None:
                logger.warning(f"Proxy failed. Trying next proxy...")
                proxy_idx += 1
                proxy = proxies[proxy_idx % len(proxies)]  # Rotate to next proxy
                success, status_msg = keep_alive(headers, email, proxy)

            # Formatting message for each account
            if success:
                messages.append(f"👤 acc: {email}\n✍️ Info: success, Point: {points:,.0f} and Keep alive [OK]")
                logger.success(f"Status: Keep alive recorded!")
            else:
                messages.append(f"👤 acc: {email}\n✍️ Info: error, Point: {points:,.0f} and Keep alive [FAILED]")
                logger.error(f"Status: {status_msg}")

            logger.info(f"Total Points: {points:,.0f}\n")

            # Rotate to the next proxy if used
            if proxy_idx is not None:
                proxy_idx += 1

        # Sending message to Telegram with total points from all users
        await telegram_message("\n".join(messages) + f"\n\nTotal points from all users: 💰 {total_points_all_users:,.0f}\n")
        countdown(180)
        logger.info(f"Restarting the process...\n")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info(f"Program terminated by user. ENJOY!\n")
