import os
import time
import json
import asyncio
from page_speed_api import GooglePageSpeed
from api_response_processor import ResponseProcessor
from urls import urls


async def write_resut_to_json(results: list) -> None:
    with open(f'{os.getcwd()}/result.json', 'w+', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)


async def main():
    start_time = time.perf_counter()
    speed_client = GooglePageSpeed()
    responses = await speed_client.get_speed_data(urls=urls)
    processor = ResponseProcessor()
    results = []
    for data in responses:
        url = processor.get_page_url(data=data)
        lighthouse_result = await processor.get_light_house_result(data)
        categorical_peroformance = await processor.get_cetegorical_performance(
            lighthouseresult=lighthouse_result
        )
        essential_metric = await processor.get_essential_metrics(
            lighthouseresult=lighthouse_result
        )
        device = processor.get_diagnosis_device(lighthouseresult=lighthouse_result)
        results.append(
            {**url, **categorical_peroformance, **essential_metric, ** device}
        )

    await write_resut_to_json(results=results)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"Elapsed run time: {elapsed_time} seconds")


asyncio.run(main())