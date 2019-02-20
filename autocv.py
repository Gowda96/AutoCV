import getpass
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
c_name=[]
c_emails=[]
c_status=[]
sender=""
password=""
receiver=""
c_index=[]
df=""
b_parts=[]


def login():
	print("----Make Sure You are looged to your gmail account-----")
	global sender,password
	sender=input("Enter Your Mail-Id:")
	password=getpass.getpass('Password:')

	
	
def formMsg(recv,name):
	msg=MIMEMultipart()
	msg['From']=sender
	msg['To']=recv
	msg['Subject']="Job Application"
	body=b_parts[0]+name+b_parts[1]
	msg.attach(MIMEText(body, 'plain'))
	part=addAttachment()
	msg.attach(part)
	return  msg.as_string()
	
def addAttachment():
	filename="VARUN_CV.pdf"
	attachment=open("C:/Users/Varun Gowda/Desktop/Python Projects/Resume Sender/VARUN_CV.pdf","rb")
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	return part
	
	
def getNameAndMailId():
	global c_emails,c_name,c_status,c_index,df
	df=pd.read_csv('mailDetails.csv')
	names=df['Name']
	mails=df['Mail']
	status=df['Stat']
	rows=df.shape[0]
	for i in range(0,rows):
		if status[i]==0:
			c_name.append(names[i])
			c_emails.append(mails[i])
			c_index.append(i)
			
			
def changeStatus():
	for i in range(0,len(c_name)):
		df.set_value(c_index[i],'Stat',1)
	df.to_csv('extesqt.csv',index=False)

						
def sendMail():	
	with smtplib.SMTP_SSL("smtp.gmail.com",port,context=con) as server:
		server.login(sender,password)
		for i in range(0,len(c_emails)):
			text=formMsg(c_emails[i],c_name[i])
			server.sendmail(sender,c_emails[i],text)
			changeStatus()
		
	
			

if __name__ == '__main__':
	port=465
	con=ssl.create_default_context()
	login()
	getNameAndMailId()
	b_file=open('body.txt','r')
	b_content=b_file.read()
	b_parts=b_content.split('%%%')
	sendMail()
	
	
	
