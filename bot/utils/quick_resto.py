import aiohttp
from aiohttp import BasicAuth

from quick_resto_API import quick_resto_interface as qri

from config import Config
from utils.format_response import format_transactions

import json

async def get(url, headers, auth):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False, auth=auth) as response:
            text = await response.text()
            try:
                response_json = json.loads(text)
                return response_json
            except:
                print('smth wrong:')
                print(text)


async def post(url, data, headers, auth):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers, auth=auth, ssl=False) as response:
            text = await response.text()
            try:
                response_json = json.loads(text)
                return response_json
            except:
                print('smth wrong:')
                print(text)
    
async def search_client(phone: str) -> bool:
    url = f"https://{Config.QUICK_RESTO_LAYER_NAME}.quickresto.ru/platform/online/bonuses/filterCustomers"
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }
    payload = {
        "search": phone[1:],
    }
    client = await post(url, payload, headers=headers, auth=BasicAuth(Config.QUICK_RESTO_API_USERNAME, Config.QUICK_RESTO_API_PASSWORD))
    if client["customers"]:
        return client["customers"][0].get("id")
    else:
        return False


async def create_client(first_name: str, last_name: str, phone: str) -> dict:
    url = f"https://{Config.QUICK_RESTO_LAYER_NAME}.quickresto.ru/platform/online/api/create?moduleName=crm.customer&className=ru.edgex.quickresto.modules.crm.customer.CrmCustomer"
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "comment": "Создан через бота",
        "contactMethods": [
            {
                "id": 0,
                "type": "phoneNumber",
                "value": phone
            }
        ],
        "customerGroup": {
            "id": 1,
            "version": 0,
            "name": "СТАРТ",
            "discountValue": 0,
            "promotable": False,
            "minTotalAmount": 0,
            "customerOperationLimit": 9999,
            "refId": "crm_discount-2409231102036127",
            "deleted": False,
            "groupId": 1
        },
        "tokens": [
            {
                "type": "card",
                "entry": "manual",
                "key": phone
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }
    
    response = await post(url, payload, headers, auth=BasicAuth(Config.QUICK_RESTO_API_USERNAME, Config.QUICK_RESTO_API_PASSWORD))
    return response

# async def make_token_for_client(client_id: int, phone: str) -> dict:
#     url = f"https://{Config.QUICK_RESTO_LAYER_NAME}.quickresto.ru/platform/online/api/update?moduleName=crm.customer&className=ru.edgex.quickresto.modules.crm.customer.CrmCustomer"
#     headers = {
#         'Content-Type': 'application/json',
#         'Connection': 'keep-alive'
#     }
#     payload = {
#         "id": client_id,
#         "tokens": [
#             {
#                 "type": "card",
#                 "entry": "manual",
#                 "key": phone
#             }
#         ]
#     }
#     response = await post(url, payload, headers, auth=BasicAuth(Config.QUICK_RESTO_API_USERNAME, Config.QUICK_RESTO_API_PASSWORD))
#     print(response)
#     return response

async def get_client_info(object_id: int) -> dict | bool:
    url = f"https://{Config.QUICK_RESTO_LAYER_NAME}.quickresto.ru/platform/online/api/read?moduleName=crm.customer&className=ru.edgex.quickresto.modules.crm.customer.CrmCustomer&objectId={object_id}"
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }
    response_json = await get(url, headers=headers, auth=BasicAuth(Config.QUICK_RESTO_API_USERNAME, Config.QUICK_RESTO_API_PASSWORD))
    if response_json:
        return response_json
    else:
        return False

async def get_bonus_programms() -> list:
    url = f"https://{Config.QUICK_RESTO_LAYER_NAME}.quickresto.ru/platform/online/api/list?moduleName=crm.settings.bonus&className=ru.edgex.quickresto.modules.crm.settings.bonus.BonusProgram"
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }
    bonuses_list = await get(url, headers=headers, auth=BasicAuth(Config.QUICK_RESTO_API_USERNAME, Config.QUICK_RESTO_API_PASSWORD))
    return bonuses_list

async def get_bonus_info(client_id: int) -> dict:
    client_info = await get_client_info(client_id)
    bonuses_list = await get_bonus_programms()

    bonus_percent = False

    for bonus_programm in bonuses_list:
        if bonus_programm['name'] == client_info['customerGroup']['name']:
            bonus_percent = bonus_programm['accValue']
            break
    if bonus_percent:
        return {
            "bonus_balance": client_info['accounts'][0]['accountBalance']['available'],
            "bonus_level": client_info['customerGroup']['name'],
            "bonus_percent": bonus_percent
        }
    else:
        return False

async def get_bonus_history(client_id: int) -> dict:
    client_info = await get_client_info(client_id)
    token = {
            "type": "phone",
            "entry": "manual",
            "key": client_info['contactMethods'][0]['value']
    }
    account_type = client_info["accounts"][0]["accountType"]

    url = f"https://{Config.QUICK_RESTO_LAYER_NAME}.quickresto.ru/platform/online/bonuses/operationHistory"
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }
    print("-"*25)
    payload = {
        "customerToken": token,
        "accountType": account_type
    }
    print(payload)
    response = await post(url, payload, headers, auth=BasicAuth(Config.QUICK_RESTO_API_USERNAME, Config.QUICK_RESTO_API_PASSWORD))
    print(response)
    print("-"*25)
    formatted_bonus_history = format_transactions(response['transactions'])
    return formatted_bonus_history

# from quick_resto_API import QuickRestoInterface

# resto_sdk = QuickRestoInterface(login="ee499",
#                                 password="s4p4YFOZ")

# resp = resto_sdk.crm_search_client("79169621323")
# print(resp)
