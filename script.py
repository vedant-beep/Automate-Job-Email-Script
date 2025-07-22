import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
import time
import schedule
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME") # Make sure this file exists and contains the hr_contacts table
LIMIT = os.getenv("LIMIT")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RESUME_PATH = os.getenv("RESUME_PATH") # The path to your resume
YOUR_NAME = os.getenv("YOUR_NAME") # Your name for the email body
YOUR_PHONE_NUMBER = os.getenv("YOUR_PHONE_NUMBER") # Your phone number for the email body
YOUR_LINKEDIN_URL = os.getenv("YOUR_LINKEDIN_URL") # Your LinkedIn for the email body
YOUR_CURRENT_ORGANIZATION = os.getenv("YOUR_CURRENT_ORGANIZATION") # Your LinkedIn for the email body


def create_email(sender_email, recipient_email, hr_name, hr_company, your_name, attachment_path=""):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Subject line personalization
    subject = f"Job Application: {your_name} - Seeking Opportunities at {hr_company}"
    msg['Subject'] = subject

    body = f"""\
    <html>
    <body>
    <p>Dear {hr_name},</p>

    <p>I hope this email finds you well.</p>

    <p>My name is {your_name}, and I am a highly motivated professional currently working in <strong>{YOUR_CURRENT_ORGANIZATION}</strong> having <strong>2.5+ years of experience</strong> (<strong>Full Stack Developer</strong>) with expertise in <strong>Java Springboot, and React and also worked in Python</strong>.</p>
    <p>I am actively exploring new opportunities where I can leverage my skills to contribute to a dynamic organization like <strong>{hr_company}</strong>.</p>

    <p><strong>I have attached my detailed resume for your review</strong>. I would be grateful if you could consider me for any matching job opportunities that arise within your company.

    Thank you for your time and consideration. I look forward to the possibility of discussing how my background aligns with your hiring needs.</p>

    <p>Best regards,</p>
    <p>{your_name}<br>
    {YOUR_PHONE_NUMBER}<br>
    {YOUR_LINKEDIN_URL}</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    # Attach resume
    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=RESUME_PATH)
            part['Content-Disposition'] = f'attachment; filename="{RESUME_PATH}"'
            msg.attach(part)
    except FileNotFoundError:
        print(f"Error: Resume file not found at {attachment_path}. Please check the path.")
        return None
    except Exception as e:
        print(f"Error attaching file: {e}")
        return None

    return msg

def send_email(sender_email, sender_password, recipient_email, email_message):
    try:
        # For Gmail: smtp.gmail.com, port 587 (TLS) or 465 (SSL)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587 # or 465 for SSL

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() # Enable TLS encryption
            server.login(sender_email, sender_password)
            text = email_message.as_string()
            server.sendmail(sender_email, recipient_email, text)
        print(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        return False


# def automated_job_application():
#     sender_email = "your_email@gmail.com"  # Your sending email address
#     sender_password = "your_app_password"  # Use an App Password if 2FA is on
#     resume_path = "path/to/your/resume.pdf" # Make sure this path is correct
#
#     try:
#         hr_data = pd.read_csv("hrs.csv")
#     except FileNotFoundError:
#         print("Error: hrs.csv not found. Please create the file.")
#         return
#
#     emails_sent_today = 0
#     max_emails_per_day = 300 # Set your daily limit
#
#     for index, row in hr_data.iterrows():
#         if emails_sent_today >= max_emails_per_day:
#             print(f"Reached daily limit of {max_emails_per_day} emails. Stopping for today.")
#             break
#
#         hr_name = row['Name'] if 'Name' in row else 'Hiring Manager' # Default if name not available
#         hr_email = row['Email']
#         hr_company = row['Company'] if 'Company' in row else 'a reputable company' # Default if company not available
#
#         # Create the email message
#         msg = create_email(sender_email, hr_email, hr_name, hr_company, "Your Name", resume_path)
#         if msg:
#             if send_email(sender_email, sender_password, hr_email, msg):
#                 emails_sent_today += 1
#             time.sleep(5) # Add a delay to avoid triggering spam filters (adjust as needed)
#
#         # Optional: Remove or mark sent emails to avoid re-sending
#         # You'd need to manage this in your CSV or a separate database
#         # For simplicity, this example just iterates through the list.
#         # For a production system, you'd load unsent emails, send, then mark them as sent.
#
#     print(f"Automation finished. Sent {emails_sent_today} emails today.")

def automated_job_application_with_db():
    sender_email = SENDER_EMAIL  # Your sending email address
    sender_password = SENDER_PASSWORD  # Use an App Password if 2FA is on
    resume_path = RESUME_PATH  # Make sure this path is correct, e.g., "C:/Users/YourUser/Documents/MyResume.pdf"

    # 1. Fetch unsent contacts from the database
    # Limit to 100 per day as discussed for better deliverability
    contacts_to_send = get_unsent_contacts(limit=LIMIT)

    if not contacts_to_send:
        print("No unsent emails found in the database. Exiting for today.")
        return

    emails_sent_today = 0
    print(f"Attempting to send emails to {len(contacts_to_send)} contacts today.")

    for contact in contacts_to_send:
        contact_id, hr_name, hr_company, hr_email = contact
        hr_email = hr_email.strip()

        msg = create_email(sender_email, hr_email, hr_name, hr_company, YOUR_NAME, resume_path)

        if msg:
            if send_email(sender_email, sender_password, hr_email, msg):
                update_sent_flag(contact_id)  # Update flag in DB
                emails_sent_today += 1
            time.sleep(5)  # Delay to avoid spam flags

    print(f"Automation finished. Sent {emails_sent_today} emails today.")

def get_unsent_contacts(limit=100):
    """Fetches contacts from the database whose sent_flag is 0."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, company, email FROM company_wise_hr_contacts WHERE is_mail_sent = 0 LIMIT ?", (limit,))
        contacts = cursor.fetchall()
        conn.close()
        return contacts
    except sqlite3.OperationalError as e:
        print(f"Error connecting to database or table not found: {e}")
        print(f"Please ensure '{DATABASE_NAME}' exists and the 'company_wise_hr_contacts' table is created within it.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while fetching contacts: {e}")
        return []

def update_sent_flag(contact_id):
    """Updates the sent_flag and last_sent_date for a given contact ID."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE company_wise_hr_contacts SET is_mail_sent = 1, last_sent_date = ? WHERE id = ?",
                       (current_date, contact_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error updating sent flag for ID {contact_id}: {e}")

# # Schedule the task to run daily
# schedule.every().day.at("09:00").do(automated_job_application) # Adjust time as needed
#
# while True:
#     schedule.run_pending()
#     time.sleep(1) # Wait a minute before checking again

automated_job_application_with_db()