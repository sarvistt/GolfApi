from playwright.async_api import async_playwright
from datetime import datetime
from zoneinfo import ZoneInfo


def getCurrentDay():
    now = datetime.now(ZoneInfo("America/Winnipeg"))
    weekday = now.strftime("%A")
    month = now.strftime("%b")
    day = now.day
    return f"{weekday}, {month} {day}"


async def getCanoeClubData():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)  # 60 seconds timeout for all actions
        await page.goto(
            "https://www.winnipeg.ca/recreation-leisure/golf-courses/canoe-club"
        )
        await page.click("text=Reserve a tee time")
        await page.select_option('select[name="Date"]', getCurrentDay())
        await page.select_option('select[name="searchTime"]', "6:00 AM")
        await page.click('input[type="radio"][name="Holes"][value="9"]')
        await page.click('input[type="radio"][name="Players"][value="2"]')
        await page.click("a.next-btn")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector("a.more-times-btn", state="visible")
        await page.click("a.more-times-btn")
        html = await page.content()
        await browser.close()
        return html
