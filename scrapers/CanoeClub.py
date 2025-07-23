from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

CLUB_NAME = "Canoe Club Golf Course"
CLUB_URL = "https://www.winnipeg.ca/recreation-leisure/golf-courses/canoe-club"
CLUB_TAGS = ["9 holes", "Public", "Pro Shop", "Power Cart Rentals", "Equipment Rentals", "Tournament Bookings", "Licensed"]

def _parseHTMLContent(html):
    soup = BeautifulSoup(html, "html.parser")
    tee_times = []
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

        tee_times.append({"time": times, "price": price})

    return tee_times

# Current Format
# {club: "Canoe Club", price: 50, time: "6:00 am", url: "/course/canoe-club", tags: ['9 holes', '2 players']},
#
def _formatTeeTimes(teeTimes):
    formattedTeeTimes = []
    for teeTime in teeTimes:
        formattedTeeTime = {}
        formattedTeeTime["club"] = CLUB_NAME
        formattedTeeTime["url"] = CLUB_URL
        formattedTeeTime["tags"] = CLUB_TAGS
        formattedTeeTime["price"] = teeTime.get("price", "N/A")
        formattedTeeTime["time"] = teeTime.get("time", "N/A")
        formattedTeeTimes.append(formattedTeeTime)
    return formattedTeeTimes

async def _getCanoeClubData(requestData):
    print('Fetching Canoe Club data...')
    async with async_playwright() as p:
        print(f"Request Data: {requestData}")  # Debugging line
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)  # 60 seconds timeout for all actions
        await page.goto(
            "https://www.winnipeg.ca/recreation-leisure/golf-courses/canoe-club"
        )
        await page.click("text=Reserve a tee time")
        await page.select_option('select[name="Date"]', requestData.date)
        await page.select_option('select[name="SearchTime"]', requestData.search_time)

        await page.evaluate(f"""
                () => {{
                    const radio = document.querySelector('input[type="radio"][name="Holes"][value="{requestData.holes}"]');
                    if (radio) {{
                        radio.checked = true;
                        radio.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }}
            """)

        await page.evaluate(f"""
                () => {{
                    const radio = document.querySelector('input[type="radio"][name="Players"][value="{requestData.players}"]');
                    if (radio) {{
                        radio.checked = true;
                        radio.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }}
            """)

        await page.click("a.next-btn")

        await page.wait_for_timeout(1000)  # Wait 1 second

        await page.evaluate("""
        () => {
            const btn = document.querySelector('a.more-times-btn');
            if (btn) btn.click();
        }
        """)

        await page.wait_for_timeout(1000)  # Wait 1 second

        return await page.content()


async def getData(requestData):
    html = await _getCanoeClubData(requestData)
    parsed_data = _parseHTMLContent(html)
    formattedData = _formatTeeTimes(parsed_data)
    return formattedData
