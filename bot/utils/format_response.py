from datetime import datetime

op_type = {
    "CREDIT": "Зачисление",
    "DEBIT": "Списание"
}

def format_transactions(transactions):
    '''
    [
        {
            "id": 1,
            "regTime": "2024-09-23T08:08:38.142Z",
            "type": "CREDIT",
            "amount": 200.00,
            "ledger": 200.00,
            "available": 200.00,
            "ownerId": 1
        }
    ],
    '''
    formatted_transactions = "ИСТОРИЯ ТРАНЗАКЦИЙ\n\n"
    for transaction in transactions[:20]:
        # print("DATE", transaction["regTime"])
        if op_type.get(transaction["type"]):
            formatted_transactions += f"""{op_type.get(transaction["type"])} {transaction["regTime"][:10]} {transaction["amount"]}\n"""
    if formatted_transactions:
        print(formatted_transactions)
        return formatted_transactions
    else:
        return "Пока что тут ничего нет("
