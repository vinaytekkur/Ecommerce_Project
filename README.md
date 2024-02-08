# Ecommerce_Project
Using Python implemented complete end-to -end ETL with transformation and validation steps.

**Project Architecture:**
![Python_ETL_Project](https://github.com/vinaytekkur/Ecommerce_Project/assets/156997918/201662e1-5913-4bc2-8ee2-f543d2c5de82)

**Source:**
  Incoming files: Every day orders data will be uploaded to incoming files folder, all these categorized based on date folder (example: for 24th jan files uploaded into folder 20240124)

**Problem Staement:**
There is a online mart called namasteMart operating in Bangalore and Mumbai. Everday all the transactions/orders files are generated and sent to us for validation and transformation.
we need to verify all the files and notify business in case of any issues.

**Validations to perform:**
1- product id should be present in product master table.
2- total sales amount should be (product price from product master table * quantity).
3- the order date should not be in future.
4- any field should not be empty.
5- The orders should be from Mumbai or Bangalore only.

**Failed Files:**
if any single orders validation fail then full file should be rejected and that files should go to rejected_files -> YYYYMMDD folder 

for each rejected file there should be one more file created in the same folder rejected_files-> YYYYMMDD folder with name error_{rejected_file_name}. 
In this file only order records should be there which failed the validation and there should be one more column for each record specifying the reason of rejection
if there are more than one reason of reject for a particular order then both should be there ; separated.

**Success Files:**
Files which passed all required validation then file should be loaded into success_files folder.

**Additional Requirement:**
after processing all the files there should be an email sent to business. In the email mention below details 
total 10 incoming files , 8 successsful files and 2 rejected files for that day.

Project walkthrough with example:
Step 1:
We received 3 orders files in "Incoming Files" folder
![image](https://github.com/vinaytekkur/Ecommerce_Project/assets/156997918/e32b680d-a783-47f8-ac0d-b836fd2a98e9)

orders_1 files couple of issues.
Issue 1: City not Bangalore or mumbai
Issue 2: Order date contains future date(2028 year year date observed)
Issue 3: Sales amount in incorrect.
![image](https://github.com/vinaytekkur/Ecommerce_Project/assets/156997918/422415e0-7efc-4e88-a4a9-f0a1cb45decd)

Remaining 2 files does not have issues.Hence moved to "Success_Files" folder
![image](https://github.com/vinaytekkur/Ecommerce_Project/assets/156997918/c159c2c7-9f1b-4d98-9a7e-c4639c822316)

Hence order_1 will move into Failed_Files folder:
![image](https://github.com/vinaytekkur/Ecommerce_Project/assets/156997918/2d0cd9f7-b5f0-4b97-afef-bbffd0750743)

Error file has information about each row why it is rejected.
![image](https://github.com/vinaytekkur/Ecommerce_Project/assets/156997918/52208b53-807f-4e43-91ce-2b972e6f29bd)

Finally Mail will be sent to respective stakeholders to answer how many files exists and how many failed/succeded etc.

Entire code implemented on Pythone using following libraries:
1) os module (to list directories, creating directory, check path exists etc)
2) csv module (to perform operations related to csv files)
3) shutil module (to copy file from one location to another location)
4) datetime (to work on date time, creating folder dates based on time of execution)

This process can be scheduled and based on automation in mind script implemented.

Thanks for reading this or checking my repo, Please reach out to me if you have any queries related to same. 














