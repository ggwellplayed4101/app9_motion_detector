import smtplib
import imghdr
from email.message import EmailMessage

# Google password for this app
PASSWORD = "mwlf xkug lyse eyax"
SENDER = "ggwellplayed4101@gmail.com"
RECIEVER = "bhargavchataut101@gmail.com"

def send_email(image_path):
    print("send email function started")
    # Create object which can mail attachments 
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey we just saw a new customer!")

    # Read binary info of the image
    with open(image_path, "rb") as file:
        content = file.read()

    # Subtype refers to metadata in an image 
    email_message.add_attachment(content, 
                                 maintype="image", 
                                 subtype=imghdr.what(None, content))
    
    
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECIEVER, email_message.as_string())
    gmail.quit()
    print("send email function ended")

if __name__ == "__main__":
    send_email(image_path="images/7.png")