import streamlit as st
import requests
import json
import time
import streamlit.components.v1 as components
import math
from datetime import datetime
import pytz






# Define the app title
st.title('The Soul Universe for Robi-Airtel Balance')

##################---For Session Key--------------################################
################## Menu Hide #################
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

########## END #############
########################## Total History Finder for Daily ############################




##################### End Total History Finder ####################
# with st.spinner('Wait for the Balance Search Counting...'):
url = "https://mistersoul.xyz/streamlit/balancesearchhistory.php?user=admin"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
json_object = json.loads(response.text)
print(json_object["balance"])
# Get Bangladesh timezone
bangladesh_tz = pytz.timezone('Asia/Dhaka')

# Get current UTC time
now_utc = datetime.now(pytz.utc)

# Convert UTC time to Bangladesh time
now_bangladesh = now_utc.astimezone(bangladesh_tz)

# Print formatted date and time
st.warning(f"Last Update Time: {now_bangladesh.strftime('%d-%m-%Y %H:%M:%S')}") 
st.success(f"Total Search Today: {json_object['balance']}")


 ##################### Token Set ####################

url = "https://apigate.robi.com.bd/token"

payload = 'username=MIFE_ATLifestyle_IGW&password=ATLifestyle%4012345&scope=PRODUCTION&grant_type=password'
headers = {
'Authorization': 'Basic SXpBTmVYd3ZiNFBhV3pEY0lMWWVLMlFMdTJjYTp6M3NiR1h2TDhZd0IyZ3poMlZZUWthcmxIT2th',
'Content-Type': 'application/x-www-form-urlencoded',
'Cookie': 'BIGipServerpool_apigate_8243=!WW8peDOdTzQhKE5NdGmKGlRP7kSE7qNjPKi2l3R/48VplQZXxRwn4vNncGFTXeqVjxBvvs3RTsEMOg==; TS01316561=01c9bf80bb5500f242765c4956e4d4a0318bf36c4cad582e76f9332fe041374d83d010fa3b8f2cc1b3a38fffce453e06c14cfc1e3f'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

json_object = json.loads(response.text)

access_token = json_object['access_token']

print(access_token)


##################--------End--------------#######################

# Create a text input box
number = st.text_input('Enter a MSISDN without 880')

# Create a button that triggers the API call
if st.button('Get Details'):
    if len(number) == 10:
        with st.spinner('Wait for the Balance and Package Details...'):
            url = "https://apigate.robi.com.bd/ocsIntegrationEnquiry/v1/integrationEnquiry?SubscriberNo="+number

            payload = 'CommandId=QueryBalance&RequestType=Event&TransactionId=243324343243&Version=3'
            headers = {
            'Authorization': 'Bearer '+access_token,
            'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)
            json_object = json.loads(response.text)

            try:
                url = "https://mistersoul.xyz/streamlit/balancehit.php?number=0"+number

                payload = {}
                headers = {}

                response = requests.request("GET", url, headers=headers, data=payload)
            except:
                print("Data Store Server is Down")


            print(f"{number}")

            # Display the API response
            if response.ok:
                if(json_object['IntegrationEnquiryResult']):

                    st.write("Mobile: 0"+number)
                    ### Balance
                    try:
                        for record in json_object["IntegrationEnquiryResult"]["BalanceRecordList"]["BalanceRecord"]:
                            if record["AccountType"] == "2000":
                                balance = int(record["Balance"])/10000
                                st.write("Sim Type: Prepaid")
                                st.write(f"Balance: {balance:.2f} TK")
                                break
                            elif record["AccountType"] == "3000":
                                balance = int(record["Balance"])/10000
                                st.write("Sim Type: Postpaid")
                                st.write(f"Balance: {balance:.2f} TK")
                                balance = int(record["AccountCredit"])/10000
                                st.write(f"Limit: {balance:.2f} TK")
                                break
                    except:
                        record = json_object["IntegrationEnquiryResult"]["BalanceRecordList"]["BalanceRecord"]
                        balance = int(record["Balance"])/10000
                        st.write(f"Balance: {balance:.2f} TK")
                        


                    ###### Last Recharge Amount
                    for record in json_object["IntegrationEnquiryResult"]["SubscriberInfo"]["Subscriber"]['SimpleProperty']:
                        if record["Id"] == "C_SUB_LASTRECHARGEAMT":
                            balance = int(record["Value"])/100
                            st.write(f"Last Recharge Amount: {balance:.0f} TK")
                            break

                   
                    ###### Last Recharge Date
                    for record in json_object["IntegrationEnquiryResult"]["SubscriberInfo"]["Subscriber"]['SimpleProperty']:
                        if record["Id"] == "C_SUB_LASTRECHARGETIME":
                            balance = record["Value"]
                            st.write(f"Last Recharge Date: {balance[0:4]}-{balance[4:6]}-{balance[6:8]} ")
                            break

                   
                    ###### Sim Bar Status
                    record = json_object["IntegrationEnquiryResult"]["SubscriberState"]
                    if record["LossFlag"] == '0':
                        st.write(f"Bar Status: Sim Active")
                    else:
                        st.write(f"Bar Status: Sim is Barred")
                    
                    st.header("Active Packge List:")
                    st.write("------------------------------------------")
                    for record in json_object["IntegrationEnquiryResult"]["BalanceRecordList"]["BalanceRecord"]:
                        try:

                        
                            if record["UnitType"] == "2":

                                st.write(f"Package Name : {record['BalanceDesc']}")

                                balance = int(record["Balance"])/60
                                st.write(f"Balance: {balance:.2f} Mins")
                                exdate = record['ExpireTime']
                                st.write(f"Expire Date: {exdate[0:4]}-{exdate[4:6]}-{exdate[6:8]} ")
                                st.write("------------------------------------------")

                            elif record["UnitType"] == "3":

                                st.write(f"Package Name : {record['BalanceDesc']}")

                                balance = int(record["Balance"])
                                balance = round(balance / math.pow(2, 30), 2)
                                st.write(f"Balance: {balance} GB")
                                exdate = record['ExpireTime']
                                st.write(f"Expire Date: {exdate[0:4]}-{exdate[4:6]}-{exdate[6:8]} ")
                                st.write("------------------------------------------")
                                

                        
                            elif record["UnitType"] == "4":

                                st.write(f"Package Name : {record['BalanceDesc']}")

                                balance = int(record["Balance"])
                                st.write(f"Balance: {balance:.2f} SMS")
                                exdate = record['ExpireTime']
                                st.write(f"Expire Date: {exdate[0:4]}-{exdate[4:6]}-{exdate[6:8]} ")
                                st.write("------------------------------------------")
                        except:
                            continue       

                    

                            

                    


                   
                else:
                    st.warning("No Data Found")



            else:
                st.write('An error occurred.')
    elif len(number) != 11:
        i=1
        print('number is not 11 digit')
        with st.spinner('Wait for the Result...'):
            url = "http://86.16.248.42:8000/gp/nidfinder.php?mobile="+number

            payload = {}
            headers = {
            
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            json_data = json.loads(response.text)
            print(f"{number}")

            # Display the API response
            if response.ok:
                st.write("NID:  "+number)
                for item in json_data:
                    st.write(f"{i}-> 0{item['customerMsisdn']}")
                    i=i+1
                i=1
            else:
                st.write('An error occurred.')
    else:
        st.write('Please enter a number.')

