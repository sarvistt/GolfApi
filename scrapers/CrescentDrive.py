from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


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


async def _getCrescentDriveData(requestData):
    async with async_playwright() as p:
        print(f"Request Data: {requestData}")  # Debugging line
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(6000)  # 60 seconds timeout for all actions
        await page.goto(
            "https://www.winnipeg.ca/recreation-leisure/golf-courses/crescent-drive"
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
    html = await _getCrescentDriveData(requestData)
    parsed_data = _parseHTMLContent(html)
    parsedTeeTimes = {"course": "Crescent Drive", "tee_times": parsed_data}
    return parsedTeeTimes
