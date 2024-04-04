from fastapi import FastAPI,File, UploadFile, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import re
import random
from uuid import uuid4
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, FileResponse
import pdfkit
from imessage_reader import fetch_data



app = FastAPI()

origins = [
    
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000/",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)


def get_mpesa_message():
    df = pd.read_excel("/Users/munanuman/Documents/sch/iMessage-Data.xlsx")
    df = df[df['User_ID']=="MPESA"]

    random.seed(30)
    df['category'] = [random.choice( ["Grocery", "Travelling", "Miscellaneous", "House expenses"]) for _ in range(len(df))]
    df = df[['Message', 'Date', 'category']]

    return df
    
# df = /Users/munanuman/Documents/sch/iMessage-Data.xlsx

# # Create a FetchData instance
# fd = fetch_data.FetchData(DB_PATH)

# # Store messages in my_data
# # This is a list of tuples containing user id, message and service (iMessage or SMS).
# my_data = fd.get_messages()
# print(my_data)

def monance_data(messages):

    monance = {}
    payments = []
    transactions = []
    dates_list = list(messages['Date'])
    category_list = list(messages['category'])

    for message, date, category in zip(messages['Message'], dates_list, category_list):

        if isinstance(message, str):
            m = message.split()[2:]

            if m[1] == "sent":
                user = re.search(r"sent to ([\w\s]+?)\s\d", message).group(1)
                payment = float(m[0][3:].replace(',', ''))
                payments.append(payment)
                
                transaction_cost_match = re.search(r'Transaction cost, Ksh([\d,.]+)', message)
                
                if transaction_cost_match:
                    transaction_cost = float(transaction_cost_match.group(1).replace(',', '').rstrip('.'))
                    transactions.append(transaction_cost)
                    
                else:
                    transaction_cost = 0.0
                UUID = str(uuid4())[:18].upper()
                monance[UUID] = {'payment': payment, 'user': user, 'date': date, 'transaction_cost': transaction_cost, 'category': category}

            elif m[1] == "paid":
                user = re.search(r"paid to ([\w\s]+)\.", " ".join(m[:9])).group(1)
                payment = float(m[0][3:].replace(',', ''))
                payments.append(payment)
                
                transaction_cost_match = re.search(r'Transaction cost, Ksh([\d,.]+)', message)
                
                if transaction_cost_match:
                    transaction_cost = float(transaction_cost_match.group(1).replace(',', '').rstrip('.'))
                    transactions.append(transaction_cost)
                else:
                    transaction_cost = 0.0
                UUID = str(uuid4())[:18].upper()
                monance[UUID] = {'payment': payment, 'user': user, 'date': date,'transaction_cost': transaction_cost, 'category': category}

    return monance, payments, transactions



@app.get("/")
async def root(dateq: str | None = None, category: str | None = None , pdf: str | None = None):
    messages = get_mpesa_message()

    if dateq:
        messages["Date"] = pd.to_datetime(messages["Date"])
        messages = messages[messages['Date'] >= pd.to_datetime(dateq)]
    
    if category:
        messages = messages[messages['category'] == category]

    monance, payments, transactions = monance_data(messages)
    response = {
        "messages": monance,
        "total_transactions": sum(transactions),
        "total_payments": sum(payments),
         "total_expense": sum(payments + transactions)
    }
    if pdf:
        df=pd.DataFrame(monance).T
        df.to_html("output/monance.html")
        pdfkit.from_file("output/monance.html", "output/monance.pdf")
        return FileResponse("output/monance.pdf", media_type= "application/pdf" , filename="downloadfile.pdf")
        
    return response



# @app.get("/")
# async def generate_pdf(
#     dateq: str = Query(None),
#     category: str = Query(None)
# ):
#     # Generate a simple PDF (modify this according to your needs)
#     pdf_content = generate_pdf_content(dateq, category)

#     # Create a BytesIO object to store the PDF content
#     pdf_buffer = io.BytesIO(pdf_content)

#     # Return the PDF file as a response
#     return StreamingResponse(
#         pdf_buffer,
#         media_type="application/pdf",
#         headers={"Content-Disposition": "attachment;filename=generated-pdf.pdf"}
#     )

# def generate_pdf_content(selected_date, category):
#     # Modify this function to generate the actual PDF content
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer)

#     # Example content - modify this according to your needs
#     p.drawString(100, 100, f"Date: {selected_date}")
#     p.drawString(100, 80, f"Category: {category}")

#     p.save()
#     buffer.seek(0)
#     return buffer.read()
