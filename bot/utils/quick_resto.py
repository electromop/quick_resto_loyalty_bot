import aiohttp
import json

async def get(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def post(url, data, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            return await response.json()


async def client_exists(phone: str) -> bool:
    url = "https://ee499.quickresto.ru/platform/online/bonuses/filterCustomers"
    data = json.dumps({
        "search": phone
    })
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Authorization': 'Basic ZWU0OTk6czRwNFlGT1o=',
    }
    response_json = post(url=url, data=data, headers=headers)
    if response_json:
        return response_json
    else:
        return False


async def get_bonus_info(client_id: int) -> dict:
    url = ...
    response_json = get()
    return response_json


async def create_client(name: str, phone: str) -> dict:
    url = ...
    response_json = get()
    return response_json


async def get_bonus_history(cleint_id: int) -> dict:
    return "история"

async def get_client_info(client_id: int) -> dict | bool:
    url = f"https://ee499.quickresto.ru/platform/online/api/read?moduleName=crm.customer&className=ru.edgex.quickresto.modules.crm.customer.CrmCustomer&objectId={client_id}"
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Authorization': 'Basic ZWU0OTk6czRwNFlGT1o=',
    }
    response_json = get(url, headers=headers)
    if response_json:
        return response_json
    else:
        return False
    

# from quick_resto_API import QuickRestoInterface

# resto_sdk = QuickRestoInterface(login="ee499",
#                                 password="s4p4YFOZ")

# resp = resto_sdk.crm_search_client("79169621323")
# print(resp)
