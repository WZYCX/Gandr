import aiohttp
import requests
import time


# Removes certificate verification warning from requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


HOST = 'https://www.ntrs.nasa.gov'
HEADERS = {"Host": "ntrs.nasa.gov"}


class Ratelimit:

    def __init__(self, limit, minutes):
        self.limit = limit
        self.minutes = minutes
        self.called = 0
        self.num = 0

    def wait(self):
        while self.called + 60 > time.time():
            time.sleep(0.01)

    def __call__(self):
        if self.called + 60*self.minutes > time.time():
            if self.num >= self.limit:
                print("RATELIMITED! Time to wait:", self.called + 60*self.minutes - time.time())
                self.wait()
                self.called = time.time()
                self.num = 1
            else:
                self.num += 1
        else:
            self.called = time.time()
            self.num = 1


# Ratelimits are the requests per number of minutes
ratelimit = Ratelimit(500, 15)


# Sends a get request to the NTRS API asynchronously

async def async_get_json(endpoint, retry=True):
    ratelimit()
    async with aiohttp.ClientSession() as session:
        async with session.get(HOST + endpoint, headers=HEADERS, ssl=False) as response:
            if response.status != 200:
                print(response.status, response.text)
                if retry:
                    ratelimit.wait()
                    await async_get_json(endpoint, retry=False)
                else:
                    return None
            return await response.json()


async def async_get_text(endpoint, retry=True):
    ratelimit()
    async with aiohttp.ClientSession() as session:
        async with session.get(HOST + endpoint, headers=HEADERS, ssl=False) as response:
            if response.status != 200:
                print(response.status, response.text)
                if retry:
                    ratelimit.wait()
                    await async_get_text(endpoint, retry=False)
                else:
                    return None
            return await response.text()


# Sends a get request to the NTRS API

def get(endpoint, retry=True):
    ratelimit()
    response = requests.get(
        HOST + endpoint,
        headers=HEADERS,
        verify=False
    )
    if response.status_code != 200:
        # print(response.status_code, response.text)
        if retry:
            ratelimit.wait()
            get(endpoint, retry=False)
        else:
            return None
    return response