import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import json
import sys

CONFIG_FILE = Path('config.json')


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


async def create_account(url):
    creds = load_config()
    email = creds.get('yahoo_email')
    password = creds.get('yahoo_password')
    if not (email and password):
        print('Yahoo credentials missing in config.json')
        return
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            # Placeholder for account creation logic
            await asyncio.sleep(1)
            await browser.close()
            print(f'Visited {url} for account creation')
    except Exception as e:
        print(f'Error creating account on {url}: {e}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python account_creation.py <url>')
    else:
        asyncio.run(create_account(sys.argv[1]))
