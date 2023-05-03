import os
import smtplib

from dotenv import load_dotenv

load_dotenv()


class EmailHandler:
    sender = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASS")
    subject = "ISS Flyover"
    message = f"""
                    From: ISS Now{sender}
                    Subject: {subject}\n
                    International Space Station can be seen at your location now!         
    
    """

    def send_email(self, receiver):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        try:
            server.login(self.sender, self.password)
            server.sendmail(self.sender, receiver, self.message)
            print("Email has been sent")
        except Exception as ex:
            print(f"{ex}\nCheck login and password")


if __name__ == "__main__":
    e = EmailHandler()
    e.send_email(os.getenv("RECEIVER"))