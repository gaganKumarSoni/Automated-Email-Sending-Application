import json
import imghdr
import smtplib
from email.message import EmailMessage

EMAIL_ADD, EMAIL_PASS = '',''
port,smtp_hos = 0,''

f=open('data.json','r')
json_data=json.load(f)
t = json.dumps(json_data['mailJson'])                                                      # mailJson dict in string format
t = t.replace('[','')
t = t.replace(']','')

for key in json_data['object']:
    if ("obj."+key) in t:
        t=t.replace(("obj."+key),json_data['object'][key])
    elif key=='assetPropertyList':
        for various_dict in json_data['object'][key]:
            if various_dict['assetTypePropertyName'] in t:
                t=t.replace( ("obj.prop."+various_dict['assetTypePropertyName']), various_dict['assetPropertyValue'])
f.close()
# eval() use to convert string to dictionary object
data1=eval(t)

if data1["from"] is None or data1["password"] is None:                                        # Use Default Parameter here
    EMAIL_ADD = ""
    EMAIL_PASS = ""
if len(data1["smtp_host"]) < 2:
    smtp_hos = 'smtp.gmail.com'
if data1["port"] is None:
    port = 465
msg = EmailMessage()
msg['Subject'] = data1["subject"]
msg['From'] = EMAIL_ADD
msg['To'] = data1["to"] 
msg['Cc'] = data1["cc"]
msg.set_content(data1['body']+"\n Attachments :")

# To WORK with MULTIPLE ATTCHMENTS FILE
# OUR JSON contain path to multiple files which store inside a list
list_of_attachments = list(data1['mailJson']['attachment'].split(','))      # attchment = is a string contain path to files, seprated by comma
for attachment in list_of_attachments:
    with open(attachment, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)      # multiple file attached

# For PDF purpose
# from pdf_mail import sendpdf
# sendpdf(sender_email_add,recer_email_add, sender_email_pass, subj_of_email, body_of_email, filename, location_of_file) 

try:
    with smtplib.SMTP_SSL(smtp_hos, port) as smtp:
        smtp.login(EMAIL_ADD, EMAIL_PASS)                                                     # msg parameter when email Msg absent
        smtp.send_message(msg, from_addr=EMAIL_ADD, to_addrs='gagansoni0054@gmail.com')
        print("Message Sent")
except Exception as e:
    print("Error Occured  :",e)