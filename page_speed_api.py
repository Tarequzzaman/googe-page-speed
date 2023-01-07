import aiohttp
import asyncio

class GooglePageSpeed:
    def __init__(self) -> None:
        self.SPEED_URL: str = (
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        )
        self.CATEGORIES: list = [
            "performance",
            "accessibility",
            "best-practices",
            "seo",
        ]
        self.STRATEGIES: str = ["DESKTOP", "MOBILE"]

    async def prepare_params(self, requested_url, strategy):
        """Generate Params for Google Speed API"""
        return {
            "url": requested_url,
            # "key": apikey, #In order to get better concurrency you need to generate a key
            "category": self.CATEGORIES,
            "strategy": strategy,
        }

    async def call_api(self, requested_url: str, strategy: str):
        """Call Google Speed API"""
        parms = await self.prepare_params(
            requested_url=requested_url, strategy=strategy
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(self.SPEED_URL, params=parms) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {}

    async def get_speed_data(self, urls) -> list:
        """Call The API asyncronously"""
        results = await asyncio.gather(
            *[
                self.call_api(url, STRATEGY)
                for STRATEGY in self.STRATEGIES
                for url in urls
            ]
        )
        return results