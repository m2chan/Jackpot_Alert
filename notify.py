# Notifies subscribers using email and text based on their notification preferences

from lotto_data import retrieve_data
from generate_messages import generate_text, generate_email
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from datetime import date
from database import create_connection
import sys
import config

def send_sms(phone_number, body_message, my_phone_number):
	'''
	Calls the Twilio API to send a text message to the subscriber
	
	Input arguments:
		phone_number: Subscriber's phone number
		body_message: Contents of text message
		my_phone_number: Private Twilio phone number
	'''
	
	phone_number = '+1' + phone_number

	account_sid = config.api_key
	auth_token = config.token
	client = Client(account_sid, auth_token)

	message = client.messages \
				.create(
					 body=body_message,
					 from_=my_phone_number,
					 to=phone_number
				 )

def send_email(receiver_email, body_message, email_password): 
	'''
	Sends an email to the subscriber using 
	
	Input arguments:
		phone_number: Subscriber's phone number
		body_message: Contents of text message
		email_password: Private Jackpot Alert email password
	'''

	port = 465
	email = 'jackpot.alert.notification@gmail.com'
	password = email_password
	smtp_server = 'smtp.gmail.com'
	message = MIMEMultipart('alternative')

	message['Subject'] = 'Jackpot Alert notification'
	message['From'] = 'Jackpot Alert'
	message['To'] = receiver_email
	html = body_message

	# Turn these into plain/html MIMEText objects
	html_body = MIMEText(html, "html")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(html_body)

	# Create a secure SSL context
	context = ssl.create_default_context()

	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(email, password)
		server.sendmail(email, receiver_email, message.as_string())

def lotto_649_query(conn, jackpot):
	'''
	uery subscribers who want to receive Lotto 64/9 notifications for jackpots at or below this week's jackpot
	Input arguments:
		conn: Database connection object
		jackpot: The jackpot amount coming up
	'''

	curr = conn.cursor()
	curr.execute('SELECT * FROM subscribers WHERE lotto_649 = 1 AND lotto_649_threshold<=?', (jackpot,))

	rows = curr.fetchall()

	result_email = []
	result_phone = []
	
	for row in rows:
		result_email.append(('send_lotto_649', row[1], row[7]))
		result_phone.append(('send_lotto_649', row[2], row[7]))

	return result_email, result_phone

def lotto_max_query(conn, jackpot):
	'''
	Query subscribers who want to receive Lotto Max notifications for jackpots at or below this week's jackpot
	Input arguments:
		conn: Database connection object
		jackpot: The jackpot amount coming up
	'''

	curr = conn.cursor()
	curr.execute('SELECT * FROM subscribers WHERE lotto_max = 1 AND lotto_max_threshold<=?', (jackpot,))

	rows = curr.fetchall()

	result_email = []
	result_phone = []
	
	for row in rows:
		result_email.append(('send_lotto_max', row[1], row[7]))
		result_phone.append(('send_lotto_max', row[2], row[7]))

	return result_email, result_phone

def main():

	# Retrieve lottery data 
	lottery_data = retrieve_data()
	days_to_lotto_649 = (lottery_data['lotto_649']['date'] - date.today()).days
	days_to_lotto_max = (lottery_data['lotto_max']['date'] - date.today()).days
	current_lotto_649_jackpot = lottery_data['lotto_649']['jackpot']
	current_lotto_max_jackpot = lottery_data['lotto_max']['jackpot']

	Determine if there are Lotto 6/49 or Lotto Max draws within the next 2 days
	if days_to_lotto_649 < 2:
		send_lotto_649 = True
	else:
		send_lotto_649 = False

	if days_to_lotto_max < 2:
		send_lotto_max = True
	else:
		send_lotto_max = False

	# Stop if the draws are more than 2 days away - no need to contact subscribers
	if not send_lotto_649 and not send_lotto_max:
		sys.exit()

	# Create connection with subscribers database on who to contact
	database = 'subscribers.db'
	conn = create_connection(database)

	# Query subcriber contact information in database
	with conn:
		lotto_649_email, lotto_649_phone = lotto_649_query(conn, current_lotto_649_jackpot)
		lotto_max_email, lotto_max_phone = lotto_max_query(conn, current_lotto_max_jackpot)

	phone_contacts = lotto_649_phone + lotto_max_phone
	email_contacts = lotto_649_email + lotto_max_email
	
	# Text subscribers
	for contact in phone_contacts:
		if contact[0]:
			phone_number = contact[1]
			if len(phone_number) < 10: # Did not opt into receiving texts
				continue
			elif len(phone_number) > 10:
				phone_number = phone_number.replace('-', '')
				while len(phone_number) != 10:
					phone_number = phone_number[1:]
			
			message = generate_text(contact[0][5:], lottery_data, contact[2])
			send_sms(phone_number, message, config.phone_number)

	# Email subscribers
	for contact in email_contacts:
		if contact[0]:
			message = generate_email(contact[0][5:], lottery_data, contact[2])
			send_email(contact[1], message, config.email_password)
			
if __name__ == '__main__':
	main()