from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.http import Http404

import requests
import json
import structlog

logger = structlog.get_logger()


def fetchCovidCases(*args, **kwrgs):
    start_datetime = "2020-03-01T00:00:00Z"
    curr_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    logger.info("fetch_covid_cases for time: {}".format(curr_datetime))
    url = "https://api.covid19api.com/summary"
    resp = requests.get(url)
    print("status ".format(resp.status_code))
    if resp.status_code == 200:
        data = resp.json()["Countries"]
        for cdata in data:
            country_code = cdata["CountryCode"].encode("utf-8")
            total_cases = cdata["TotalConfirmed"]
            total_deaths = cdata["TotalDeaths"]
            logger.info(
                "code {}, total case {}, total deaths {}".format(
                    country_code, total_cases, total_deaths
                )
            )
            redis_key = "polls.cases.country.code:{}".format(country_code)
            cache.set(redis_key, total_cases)
            redis_key = "polls.deaths.country.code:{}".format(country_code)
            cache.set(redis_key, total_deaths)
        logger.info("covid updates successfully fetched {}".format(resp.data))
    else:
        logger.info(
            "error while fetching covid updates status {} err {}".format(
                resp.status_code, resp.text
            )
        )


def fetchCovidDeaths(*args, **kwrgs):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    pass


if __name__ == "__main__":
    fetchCovidCases()
