import pandas as pd
# Replace 'your_file.xlsx' with the actual file path of your Excel file
df = pd.read_excel('/Users/munanuman/Documents/sch/iMessage-Data.xlsx', sheet_name='iMessages')

column_names = df.columns
# print(column_names)


# Assuming the 'User_ID' column contains 'MPesa'
messages_from_mpesa = df[df['User_ID'] == 'MPESA']


import re

info = {}
dates_list = list(messages_from_mpesa['Date'])  # Convert dates to a list

for message, date in zip(messages_from_mpesa['Message'], dates_list):
    # Check if message is a string
    if isinstance(message, str):
        m = message.split()[2:]

        if m[1] == "sent":
            user = re.search(r"sent to ([\w\s]+?)\s\d", message).group(1)
            payment = float(m[0][3:].replace(',', ''))
            transaction_cost_match = re.search(r'Transaction cost, Ksh([\d,.]+)', message)
            if transaction_cost_match:
                transaction_cost = float(transaction_cost_match.group(1).replace(',', '').rstrip('.'))
            else:
                transaction_cost = 0.0
            info[user] = {'payment': payment, 'date': date, 'transaction_cost': transaction_cost}

        elif m[1] == "paid":
            user = re.search(r"paid to ([\w\s]+)\.", " ".join(m[:9])).group(1)
            payment = float(m[0][3:].replace(',', ''))
            transaction_cost_match = re.search(r'Transaction cost, Ksh([\d,.]+)', message)
            if transaction_cost_match:
                transaction_cost = float(transaction_cost_match.group(1).replace(',', '').rstrip('.'))
            else:
                transaction_cost = 0.0
            info[user] = {'payment': payment, 'date': date,'transaction_cost': transaction_cost}

info
