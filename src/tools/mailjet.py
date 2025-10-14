from mailjet_rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

def mail(user, subject, html_content):
  api_key = os.environ["MJ_APIKEY_PUBLIC"]
  api_secret = os.environ["MJ_APIKEY_PRIVATE"]
  mailjet = Client(auth=(api_key, api_secret))
  data = {
    "FromEmail": user + "@jazzin.amsterdam",
    "FromName": "Jazz in Amsterdam - " + user,
    "Subject": subject,
    "Text-part": "",
    "Html-part": html_content,
    "Recipients": [{"Email": "jazzinmokum@gmail.com"}],
  }
  result = mailjet.send.create(data=data)
  print("Email status: " + str(result.status_code))