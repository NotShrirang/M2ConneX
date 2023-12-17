from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import threading
import os
import dotenv

dotenv.load_dotenv()


class SendEmailThread(threading.Thread):
    def __init__(self, receiver, subject, message, cc=""):
        self.email = os.environ.get('EMAIL')
        self.password = os.environ.get('EMAIL_PASSWORD')
        self.receiver = receiver
        self.subject = subject
        self.message = message
        self.cc = cc
        threading.Thread.__init__(self)

    def run(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.set_debuglevel(0)
            server.ehlo()
            server.starttls()
            server.login(self.email, self.password)

            body = MIMEMultipart("alternative")
            body["Subject"] = self.subject
            body["From"] = self.email
            body["To"] = self.receiver
            body.attach(MIMEText(self.message, 'html'))
            if self.cc != "":
                body['Cc'] = self.cc
                rcpt = [self.receiver] + self.cc.split(',')
            else:
                rcpt = [self.receiver]
            server.sendmail(self.email, rcpt, body.as_string())
            return True
        except:
            return False


def send_email(receiver, subject, message, cc='', *args, **kwargs):
    SendEmailThread(receiver=receiver, subject=subject, message=message, cc=cc).start()

def send_welcome_email(name, *args, **kwargs):
    subject = "Welcome to MMCOE Alumni Portal"
    message = f"""
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body style="
            font-family: Arial, sans-serif;
            text-align: center;
        ">
    <div class="container" style="
                max-width: 600px;
                margin: 0 auto;
            ">
        <h1 style="margin-top: 2.5rem; color: #f21919;">Welcome to MMCOE Alumni Portal, <br/>{name}!</h1>
        <p style="
                    margin-top: 1.25rem;
                    font-size: 16px;
                    line-height: 1.5;
                ">
            Your account has been successfully created on MMCOE Alumni Portal!
        </p>
        <div class="social-icons" style" margin-top: 2.5rem; margin-left: 1.25rem; ">
            <a href=" https://github.com/Club-of-Developers-and-Engineers" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
            <img src="https://cdn4.iconfinder.com/data/icons/iconsimple-logotypes/512/github-256.png" alt="GitHub"
                style="
                    height: 2rem;
                    width: 2rem;
                ">
            </a>
            <a href="https://huggingface.co/code-mmcoe" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFIM-wwuz30Pnb1FYJ2OYpxuq5KZcAPNIekUVFBhraEA&s"
                    alt="Hugging Face" style="
                    height: 2rem;
                    width: 2rem;
                ">
            </a>
            <a href="https://www.instagram.com/code_mmcoe" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/instagram_circle-512.png"
                    alt="Instagram" style="
                    height: 2rem;
                    width: 2rem;
                ">
            </a>
            <a href="https://www.linkedin.com/company/75646530/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/linkedin_circle-512.png"
                    alt="LinkedIn" style="
                    height: 2rem;
                    width: 2rem;
                ">
            </a>
        </div>
    </div>

</body>
</body>

</html>
    """
    send_email(kwargs['receiver'], subject, message)

if __name__ == '__main__':
    send_welcome_email(receiver="shrirangmahajan123@gmail.com", name="Shrirang Mahajan")

