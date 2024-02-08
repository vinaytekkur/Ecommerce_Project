import datetime
import os
import csv
import shutil
import smtplib

product_master_dict = {}
city_lst = ['mumbai', 'bangalore']
with open('./Namaste_Mart/product_master.csv', 'r') as pd_ms:
    for line in pd_ms.readlines()[1:]:
        line = line.replace('\n', '')
        lst = line.split(',')
        product_master_dict[lst[0]] = int(lst[2])

prod_dict_keys = [key for key in product_master_dict.keys()]
today_date = datetime.datetime.today().strftime('%Y%m%d')
file_path = f'./Namaste_Mart/incoming_files/{today_date}'
failed_file_path = f'./Namaste_Mart/failed_files/{today_date}'
success_file_path = f'./Namaste_Mart/successful_files/{today_date}'
incoming_files_lst = os.listdir(file_path)
incoming_files_cnt = len(incoming_files_lst)
failed_file_cnt = 0
success_file_cnt = 0

for file_name in incoming_files_lst:
    with open(f'{file_path}/{file_name}', 'r') as ord_file:
        file_content = []
        order_file_dict = {}
        is_file_failed = False
        header = ord_file.readline().replace('\n', '').split(',')
        for line in ord_file.readlines():
            order_id_lst = []
            error_msg = []
            line_lst = line.replace('\n', '').split(',')
            for record in line_lst:
                # Validating any value is blank or not
                if record == '':
                    field_name = header[line_lst.index(record)]
                    error_msg.append(f'{field_name} is blank')

            # Verify Product id
            order_id_lst.append(line_lst[2])
            for order in order_id_lst:
                if order not in prod_dict_keys:
                    error_msg.append(f'{order} does not exists in products master')

            # City should only from Mumbai and Bangalore
            line_city = line_lst[5].lower()
            if line_city not in city_lst:
                error_msg.append(f'{line_city} is Invalid')

            # order date should not be of future dates
            ord_dt = str(line_lst[1])
            order_date_to_date = datetime.datetime.strptime(ord_dt, '%d/%m/%Y')
            if order_date_to_date > datetime.datetime.today():
                error_msg.append(f"{ord_dt} is invalid")

            # validate order price
            order_price_dict = {line_lst[2]: {
                    "price" : int(line_lst[4]),
                    "quantity": int(line_lst[3])
                }}

            product_master_price = product_master_dict.get(line_lst[2])
            if product_master_price is None:
                error_msg.append(f"Product id either blank or not exists hence can not perform Price calculations")
            else:
                order_item_quantity = order_price_dict[line_lst[2]]['quantity']
                final_item_price = product_master_price * order_item_quantity
                if order_price_dict[line_lst[2]]['price'] != final_item_price:
                    error_msg.append(f"Order sales incorrect,Actual value should be {final_item_price}")

            if error_msg:
                err_str = ""
                for error in error_msg:
                    err_str += error + '; '
                line_lst.append(err_str)
                is_file_failed = True
                file_content.append(line_lst)

        if is_file_failed:
            failed_file_cnt += 1
            failed_file_name = f"error_{file_name}"
            if not os.path.exists(failed_file_path):
                os.makedirs(failed_file_path)
            with open(f'{failed_file_path}/{failed_file_name}', 'w', newline='', encoding='utf-8') as failed_file:
                header.append('error_messages')
                csvwriter = csv.writer(failed_file)
                # writing the fields
                csvwriter.writerow(header)
                # writing the data rows
                csvwriter.writerows(file_content)
        else:
            success_file_cnt += 1
            if not os.path.exists(success_file_path):
                os.makedirs(success_file_path)
            shutil.copy(f'{file_path}/{file_name}', success_file_path)


def send_mail(incoming_file_cnt, failed_cnt, success_cnt):
    # creates SMTP session
    sttp_conn = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    sttp_conn.starttls()
    # Authentication
    sttp_conn.login("<sender_email_id>", "<sender_email_id_password>")
    message = f"Hi Team\n, Please consider following details:\n Total Incoming Files : {incoming_file_cnt}\n " \
              f"Total Failed Files : {failed_cnt}\n " \
              f"Total Success Files : {success_cnt}\n\n Thanks,\nVinay Tekkur"
    sttp_conn.sendmail("sender_email_id", "receiver_email_id", message)
    # terminating the session
    sttp_conn.quit()


def get_execution_details(incoming_file_cnt, failed_cnt, success_cnt):
    print("---------------------------------------------------")
    print(f"Total Incoming Files : {incoming_file_cnt}")
    print(f"Total Failed Files : {failed_cnt}")
    print(f"Total Success Files : {success_cnt}")
    print("---------------------------------------------------")


get_execution_details(incoming_files_cnt, failed_file_cnt, success_file_cnt)
send_mail(incoming_files_cnt, failed_file_cnt, success_file_cnt)
