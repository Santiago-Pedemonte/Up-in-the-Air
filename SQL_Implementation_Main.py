from SQL_Implementation_Classes import *
from SQL_Implementation_Functions import *
import json
import ast
import datetime

if __name__ == '__main__':

    information = FlightAndPassengerInformation()

    transaction_num = generate_transaction_number()
    customer_id = generate_customer_ID()
    

    info = json.loads(information.response)
    info = info[0]
    for k,v in info['arrival'].items():
        if k == "scheduledTimeLocal":
            s = v
        if k == "actualTimeLocal":
            a = v
        else:
            pass

    date_time_obj = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M-%S:%f')
    date_time_obj2 = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M-%S:%f')

    timedelta = date_time_obj-date_time_obj2

    td = (timedelta.total_seconds())
    calcDelay = td/60
    if calcDelay <= 0:
        calcDelay = 0

    write_customer(transaction_num, information.customerFirstName, information.customerLastName,
                    information.flightNumber, calcDelay, calculate_payout(calcDelay), customer_id, information.flightDate)

    print("passenger delayed (min): ", calcDelay, " passenger_owed: $", calculate_payout(calcDelay))

    update_insurance_wallet(get_wallet_change(calcDelay), transaction_num)