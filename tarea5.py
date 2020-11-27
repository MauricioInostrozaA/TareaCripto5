import imaplib
import email
import email.parser
import datetime
import time	
import re

FILE_NAME = 'archivo.csv'
# ----- Connect to the server -----
email_host='imap.gmail.com'
email_user='EMAIL@gmail.com'
email_pass='PASSWORD'

print('Connecting to', email_host)
connection = imaplib.IMAP4_SSL(email_host, 993)

# ----- Login to our account -----
print('Logging in as', email_user)
connection.login(email_user,email_pass)
print("Login Successful")

# ----- 
connection.select('INBOX')
#print(connection.select('INBOX'))

# ----- open .csv file -----
lists = [[]]
with open(FILE_NAME, newline='') as file:
	
	data = file.readlines()
	for row in data:
		parse = row.split(";", 2)
		if parse[0] == '':
			break
		parse[2] = parse[2].strip("\r\n")
		#print(str(number+))
		lists[0].append(parse[0])
		lists[0].append(parse[1])
		lists[0].append(parse[2])
		lists.append([])
		
mail = lists[0][0]
regex = lists[0][1]
date = lists[0][2]
# ----- convert date format from dd/mm/yy to dd-mm-yyyy -----
date2 = datetime.datetime.strptime(date, "%d/%m/%y").strftime("%d-%b-%Y")

# ----- some prints -----
print('___________________________________________________________________')
print('Mail remitente: ' + mail)
print('Fecha Desde: ' + date2)
print('regex utilizado: ' + regex)
print('___________________________________________________________________')

# ----- for raw testing -----
#mail = "no-reply@twitch.tv"
#date = "29-Jul-2017"
#regex = r'^[a-f0-9]{16}\-[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}\-000000@us-west-2\.amazonses\.com$'

#status, data = connection.search(None, 'FROM', '"{}"'.format(mail))
# ---------------------------

status, data = connection.search(None, '(FROM %s SINCE %s)' %(mail,date2))
datalist = data[0].decode().split()
#print(datalist)
count = 0
lenDataList = str(len(datalist))
print('Número de Email captados: ' + lenDataList)

for n in datalist:
	status, raw_data = connection.fetch(n, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
	status, raw_date = connection.fetch(n, '(INTERNALDATE)')

	# ----- change date format -----
	timestruct = imaplib.Internaldate2tuple(raw_date[0])
	str_datetime = raw_date[0].decode().split('"')[1]
	timezone_aware = email.utils.parsedate_to_datetime(str_datetime)
	date = timezone_aware.strftime("%d/%m/%Y")

	str_data = str(raw_data[0][1])[15:][:-10]

	# ----- show all data (un-comment to show all msg-id and dates from all emails)-----
	#print('Message ID: ' + str_data)
	#print('Date: ' + date)

	# ----- checking regex -----
	check = re.fullmatch(regex, str_data)

	if not check:
		count = count + 1
		# ----- showing the non-valid emails -----
		print('___________________________________________________________________')
		print('[DANGER!] Este correo no utiliza la misma expresión regular')
		print('Message ID: ' + str_data)
		print('Date: ' + date)
		print('___________________________________________________________________')

print('Número de Emails sospechosos: ' + str(count) + '/' + lenDataList)