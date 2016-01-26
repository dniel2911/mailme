import smtplib, sys, getpass
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

fromaddr = parser.get('email', 'fromaddr')
toaddr = parser.get('email', 'toaddr')

message = MIMEMultipart()

message['From'] = fromaddr
message['To'] = toaddr
if len(sys.argv)>2:
	message['Subject'] = sys.argv[1]
else:
	message['Subject'] = ''

 
body = "This is a file from MailMe"
message.attach(MIMEText(body, 'plain'))
 
filename = sys.argv[1]
attachment = open(filename, "rb")
 
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
message.attach(part)
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
print "Please enter your gmail password"
password = getpass.getpass()
server.login(fromaddr, password)
text = message.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()