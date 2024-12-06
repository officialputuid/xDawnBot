# xDawnBot
This bot connects to farm DAWN Validator using a multi account and support with/out proxies.

## Installation

1. Install ENV
   ```bash
   sudo apt update -y && apt install -y python3 python3-venv pip
   ```

2. Setup resources:
   ```bash
   git clone https://github.com/officialputuid/xDawnBot && cd xDawnBot
   python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   python3 main.py
   ```

## Config
- If you haven't registered, feel free to use my referral code: `thejskiq`
- Edit the `config.json` file in the following format:
   ```json
    {
      "telegram_bot_token": "YOUR_TOKEN_ID FROM @BotFather",
      "telegram_chat_id": "YOUR_CHAT_ID FROM @getmyid_bot",
      "appid": "YOUR_APPID FROM (Inspect - Network - getpoint)",
      "accounts": [
        {
          "email": "example@domain.com",
          "token": "get token? (Inspect - Network - getpoint - Authorization)"
        },
        {
          "email": "example2@domain.com",
          "token": "get token? (Inspect - Network - getpoint - Authorization)"
        }
      ]
    }
   ```
   - `telegram_bot_token`: The Telegram bot token obtained from @BotFather.
   - `telegram_chat_id`: The Telegram chat ID obtained from @getmyid_bot.
   - `appid`: YOUR_APPID FROM (Inspect - Network - getpoint).
   - `accounts`: Each account requires an `email` and a `token` obtained from network inspection.

## Proxy  
- Fill in `proxy.txt` with the format `protocol://user:pass@host:port`.  

## Need Proxy?
1. Sign up at [Proxies.fo](https://app.proxies.fo/ref/849ec384-ecb5-1151-b4a7-c99276bff848).
2. Go to [Plans](https://app.proxies.fo/plans) and only purchase the "ISP plan" (Residential plans don’t work).
3. Top up your balance, or you can directly buy a plan and pay with Crypto!
4. Go to the Dashboard, select your ISP plan, and click "Generate Proxy."
5. Set the proxy format to `protocol://username:password@hostname:port`
6. Choose any number for the proxy count, and paste the proxies into `proxy.txt`.

## Donations
- **PayPal**: [Paypal.me/IPJAP](https://www.paypal.com/paypalme/IPJAP)
- **Trakteer**: [Trakteer.id/officialputuid](https://trakteer.id/officialputuid) (ID)
