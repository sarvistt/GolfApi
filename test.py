from playwright.async_api import async_playwright
from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio
from bs4 import BeautifulSoup

def getCurrentDay():
    now = datetime.now(ZoneInfo("America/Winnipeg"))
    weekday = now.strftime("%A")
    month = now.strftime("%b")
    day = now.day
    return f"{weekday}, {month} {day}"

async def getCanoeClubData():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(6000)  # 60 seconds timeout for all actions
        await page.goto("https://www.winnipeg.ca/recreation-leisure/golf-courses/canoe-club")
        await page.click('text=Reserve a tee time')
        await page.select_option('select[name="Date"]', getCurrentDay())
        await page.select_option('select[name="SearchTime"]', '6:00 am')
        await page.evaluate("""
            () => {
                const radio = document.querySelector('input[type="radio"][name="Holes"][value="9"]');
                if (radio) {
                    radio.checked = true;
                    radio.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        """)

        await page.evaluate("""
            () => {
                const radio = document.querySelector('input[type="radio"][name="Players"][value="2"]');
                if (radio) {
                    radio.checked = true;
                    radio.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        """)

        await page.click('a.next-btn')

        await page.wait_for_timeout(1000)  # Wait 1 second


        await page.evaluate("""
    () => {
        const btn = document.querySelector('a.more-times-btn');
        if (btn) btn.click();
    }
""")
        
        await page.wait_for_timeout(1000)  # Wait 1 second

        return await page.content()
    
def parseHTMLContent(html):
    soup = BeautifulSoup(html, 'html.parser')
    tee_times = []
    print('Here')
    for div in soup.select('div[class^="search-results-tee-times-box"]'):
        time_tag = div.find("p", class_="time")
        if time_tag:
            times = time_tag.get_text(strip=True)
        else:
            times = "N/A"

        price_tag = div.find("p", class_="price")
        if price_tag:
            price = price_tag.get_text(strip=True)
        else:
            price = "N/A"
        
        tee_times.append({
            "time": times,
            "price": price
        })

    return tee_times

if __name__ == "__main__":
    html = asyncio.run(getCanoeClubData())
    parsed_data = parseHTMLContent(html)
    parsedTeeTimes = ({
        "course": "Canoe Club",
        "tee_times": parsed_data
    })
    print(parsedTeeTimes)