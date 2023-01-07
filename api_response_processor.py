class ResponseProcessor:
    def __init__(self) -> None:
        self.CATEGORIES: list = [
            "performance",
            "accessibility",
            "best-practices",
            "seo",
        ]
        self.ESSENTIAL_METRICS = [
            "firstContentfulPaint",
            "firstMeaningfulPaint",
            "largestContentfulPaint",
            "speedIndex",
            "interactive",
            "observedDomContentLoaded",
            "observedLoad",
            "totalBlockingTime",
            "cumulativeLayoutShift",
        ]

    def get_page_url(self, data: dict) -> dict:
        return {"page_url": data.get("id")}

    def get_diagnosis_device(self, lighthouseresult: dict) -> dict:
        return {
            "device": lighthouseresult.get("configSettings").get("emulatedFormFactor")
        }

    async def get_cetegorical_performance(self, lighthouseresult: dict) -> dict:
        """There we will get URL SCORE, PERFORMANCE, BEST_PRACTICE & SEO information"""
        return {
            category: lighthouseresult.get("categories", {})
            .get(category, {})
            .get("score", None)
            for category in self.CATEGORIES
        }

    async def get_essential_metrics(self, lighthouseresult: dict) -> dict:
        essential_metric_result = {}
        for metric in self.ESSENTIAL_METRICS:
            if (
                len(
                    lighthouseresult.get("audits", {})
                    .get("metrics", {})
                    .get("details", {})
                    .get("items", [])
                )
                > 0
            ):
                essential_metric_result[metric] = (
                    lighthouseresult.get("audits", {})
                    .get("metrics", {})
                    .get("details", {})
                    .get("items")[0]
                    .get(metric, None)
                )
            else:
                essential_metric_result[metric] = None
        return essential_metric_result

    async def get_light_house_result(self, data: dict) -> dict:
        return data.get("lighthouseResult", {})
