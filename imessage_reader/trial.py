from imessage_reader import fetch_data

DB_PATH = "/Users/muna/Documents/iMessage-Data.sqlite"


# Create a FetchData instance
fd = fetch_data.FetchData(DB_PATH)

# Store messages in my_data
# This is a list of tuples containing user id, message and service (iMessage or SMS).
my_data = fd.get_messages()
print(my_data)
