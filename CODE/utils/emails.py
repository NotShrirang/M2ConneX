from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import threading
from alumniportal.celery import app
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
        except Exception as e:
            print(e)
            return False


@app.task(bind=True)
def send_email(self, receiver, subject, message, cc='', *args, **kwargs):
    print("SENDING EMAIL TO:" + str(receiver))
    SendEmailThread(receiver=receiver, subject=subject,
                    message=message, cc=cc).start()


def send_nsfw_report_to_admins(feedId: str, userName: str, userEmail: str):
    subject = "NSFW Content Found"
    message = f"""
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>NSFW Content Found</title>
</head>

<body>
    <div style="display: flex; align-items: center; justify-content: center; flex-direction: row; gap: 1.25rem;">
        <img src="https://mmcoe.edu.in/images/mmcoe-logo.jpg" alt="MMCOE Logo" style="height: 5rem; width: 5rem; margin-left: 1.25rem; margin-top: 1.25rem;">
        <h1 style="margin-top: 2.5rem; color: #f21919;">MMCOE Alumni Portal</h1>
    </div>
        <h1>NSFW Content Found</h1>
        <h3>Dear Admin,</h3>
        <h3>We found NSFW Content in the following post.</h3>
        <br/>
        <h2>Post Details:</h2>
        <h3>FeedId: {feedId}</h3>
        <h3>Name: {userName}</h3>
        <h3>Email: {userEmail}</h3>
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
</body>
"""
    admins = ['shrirangmahajan123@gmail.com']
    for admin in admins:
        send_email.delay(admin, subject, message)


def send_nsfw_report_to_user(feedId: str, userName: str, userEmail: str, postTime: str):
    subject = "NSFW Content Found"
    message = f"""
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Found NSFW Content</title>
</head>

<body>
    <div style="display: flex; align-items: center; justify-content: center; flex-direction: row; gap: 1.25rem;">
        <img src="https://mmcoe.edu.in/images/mmcoe-logo.jpg" alt="MMCOE Logo" style="height: 5rem; width: 5rem; margin-left: 1.25rem; margin-top: 1.25rem;">
        <h1 style="margin-top: 2.5rem; color: #f21919;">MMCOE Alumni Portal</h1>
    </div>
    <h1>Found NSFW Content</h1>
    <h3>Dear {userName},</h3>
    <h3>We found NSFW Content in your previous post.</h3>
    <h3>This type of content is NOT allowed on the platform.</h3>
    <br/>
    <h2>Post Details:</h2>
    <h3>Post Id: {feedId}</h3>
    <h3>Post Time: {postTime}</h3>
    <br/>
    <h3>Your post has been deleted.</h3>
    <h3>Kindly refrain from posting such content in the future.</h3>
    <br/>
    <h3>Regards,</h3>
    <h3>MMCOE Alumni Portal Team</h3>
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
</body>
"""
    send_email.delay(userEmail, subject, message)


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
    send_email.delay(kwargs['receiver'], subject, message)


def send_opportunity_application_email(name, receiver, opportunityName, companyName):
    subject = "MMCOE Alumni Portal - Opportunity Application"
    message = f"""
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>MMCOE Alumni Portal - Opportunity Application</title>
</head>

<body>
    <div style="display: flex; align-items: center; justify-content: center; flex-direction: row; gap: 1.25rem;">
        <img src="https://mmcoe.edu.in/images/mmcoe-logo.jpg" alt="MMCOE Logo" style="height: 5rem; width: 5rem; margin-left: 1.25rem; margin-top: 1.25rem;">
        <h1 style="margin-top: 2.5rem; color: #f21919;">MMCOE Alumni Portal</h1>
    </div>
    <h1>Opportunity Application</h1>
    <h3>Dear {name},</h3>
    <h3>You have successfully applied for the following opportunity.</h3>
    <br/>
    <h2>Opportunity Details:</h2>
    <h3>Opportunity Name: {opportunityName}</h3>
    <h3>Company Name: {companyName}</h3>
    <br/>
    <h3>Regards,</h3>
    <h3>MMCOE Alumni Portal Team</h3>
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
</body>
</html>
"""
    send_email.delay([str(receiver), ], subject, message)


def send_opportunity_application_accepted_email(name, receiver, opportunityName, companyName):
    subject = "MMCOE Alumni Portal - Opportunity Application Accepted"
    message = f"""
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>MMCOE Alumni Portal - Opportunity Application Accepted</title>
</head>

<body>
    <div style="display: flex; align-items: center; justify-content: center; flex-direction: row; gap: 1.25rem;">
        <img src="https://mmcoe.edu.in/images/mmcoe-logo.jpg" alt="MMCOE Logo" style="height: 5rem; width: 5rem; margin-left: 1.25rem; margin-top: 1.25rem;">
        <h1 style="margin-top: 2.5rem; color: #f21919;">MMCOE Alumni Portal</h1>
    </div>
    <h1>Opportunity Application Accepted</h1>
    <h3>Dear {name},</h3>
    <h3>Congratulations! Your application for the following opportunity has been accepted.</h3>
    <br/>
    <h2>Opportunity Details:</h2>
    <h3>Opportunity Name: {opportunityName}</h3>
    <h3>Company Name: {companyName}</h3>
    <br/>
    <h3>Regards,</h3>
    <h3>MMCOE Alumni Portal Team</h3>
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
</body>
</html>
"""
    send_email.delay(receiver, subject, message)


def send_opportunity_application_rejected_email(name, receiver, opportunityName, companyName):
    subject = "MMCOE Alumni Portal - Opportunity Application Rejected"
    message = f"""
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>MMCOE Alumni Portal - Opportunity Application Rejected</title>
</head>

<body>
    <div style="display: flex; align-items: center; justify-content: center; flex-direction: row; gap: 1.25rem;">
        <img src="https://mmcoe.edu.in/images/mmcoe-logo.jpg" alt="MMCOE Logo" style="height: 5rem; width: 5rem; margin-left: 1.25rem; margin-top: 1.25rem;">
        <h1 style="margin-top: 2.5rem; color: #f21919;">MMCOE Alumni Portal</h1>
    </div>
    <h1>Opportunity Application Rejected</h1>
    <h3>Dear {name},</h3>
    <h3>Thank you for your application to the {opportunityName} opportunity at {companyName}.</h3>
    <h3>Unfortunately, they've chosen to not move forward with your candidacy at this time.</h3>
    <h3>Your dream job is still waiting for you.</h3>
    <br/>
    <h2>Opportunity Details:</h2>
    <h3>Opportunity Name: {opportunityName}</h3>
    <h3>Company Name: {companyName}</h3>
    <br/>
    <h3>Regards,</h3>
    <h3>MMCOE Alumni Portal Team</h3>
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
</body>
</html>
"""
    send_email.delay(receiver, subject, message)


if __name__ == '__main__':
    send_welcome_email(receiver="shrirangmahajan123@gmail.com",
                       name="Shrirang Mahajan")
