import os
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

# Send/Recieve attachments at this email
RECIEVE_EMAIL = ''
SENDER_EMAIL = ''
SENDER_PASSWORD = "123qwe123qwe!"

# Current Path
curPath = os.getcwd()

# All files/folders in directory - other than source file
allFiles = os.listdir('.')
allFiles.remove(os.path.basename(__file__))

# Remove all folders from list of what to send
for file in allFiles:
    curName = file.split('.')

    if len(curName) == 1:
        allFiles.remove(curName[0])

# Check everything in directory for errors including:
# Folders, Files >= 25000000 bytes, Total files are >= 50Mb, No files to send
MAX_FILE_SIZE = 25000000
totalSize = 0

# Remove file from send list if file is > 25Mb
for file in allFiles:
    # Size in bytes of current file
    curFileSize = os.stat('./' + file).st_size
    
    if curFileSize > MAX_FILE_SIZE:
        allFiles.remove(file)
    # Keeps track of total email size
    else:
        totalSize += curFileSize

# Attachments size total is too large
if totalSize > MAX_FILE_SIZE:
    print('Email too large, exiting')
    exit()

# instance of MIMEMultipart 
msg = MIMEMultipart() 
  
msg['From'] = SENDER_EMAIL
msg['To'] = RECIEVE_EMAIL
msg['Subject'] = "Python Script Email Sender"
  
print(allFiles)

# Set every non empty valid file as an attachment
for file in allFiles:
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(file, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(file)))
    msg.attach(part)

# Send email
s = smtplib.SMTP('smtp.gmail.com', 587) 
s.starttls() 
s.login(SENDER_EMAIL, SENDER_PASSWORD) 
s.sendmail(SENDER_EMAIL, RECIEVE_EMAIL, msg.as_string()) 
s.quit() 