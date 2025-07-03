from scrapers.CanoeClub import getData as getCanoeClubData
from scrapers.CrescentDrive import getData as getCrescentDriveData
import asyncio


class ScrapCompiler:
    def __init__(self, requestData):
        self.requestData = requestData
        self.scrapers = [
            getCanoeClubData,
            getCrescentDriveData
        ]

    async def compileAll(self):
        # Run all scrapers concurrently, skipping any that raise exceptions
        tasks = [scraper(self.requestData) for scraper in self.scrapers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # Filter out exceptions, keep only successful results
        successful = [result for result in results if not isinstance(result, Exception)]
        return successful
