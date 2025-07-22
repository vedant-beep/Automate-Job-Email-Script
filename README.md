Automated HR Email Outreach Script
==================================

This Python script automates the process of sending personalized job application emails to HR contacts listed in a SQLite database. It tracks which emails have been sent to avoid duplicates and uses environment variables for secure credential management.

Features
--------

*   Reads HR contact details (Name, Company, Email) from a SQLite database.
    
*   Sends personalized HTML emails with bold formatting.
    
*   Attaches your resume (PDF) to each email.
    
*   Updates a is_mail_sent in the database for each successfully sent email.
    
*   Limits the number of emails sent per daily run (e.g., 100 emails) to manage deliverability and avoid spam flags.
    
*   Uses environment variables to securely store sensitive information like email credentials and file paths.
    
*   Can be scheduled to run daily using the schedule library.
    

Prerequisites
-------------

Before you begin, ensure you have the following installed:

*   **Python 3.x**: Download from [python.org](https://www.python.org/downloads/).
    
*   **Git** (optional, for cloning the repository): Download from [git-scm.com](https://git-scm.com/downloads).
    

Setup Instructions
------------------

Follow these steps to set up and run the project on your local machine.

### 1\. Clone the Repository (if applicable)

If this project is hosted on Git, clone it:
```bash 
git clone <repository_url> 
cd <project_directory>
```

Otherwise, navigate to the folder where you have your `script.py` and other project files.

### 2\. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash 
python -m venv venv  # Creates a virtual environment named 'venv'
```

Activate the virtual environment:

*   Bash.\\venv\\Scripts\\activate
    
*   Bashsource venv/bin/activateYou should see (venv) in your terminal prompt.
    

### 3\. Install Dependencies

With your virtual environment activated, install the required Python libraries:

```bash 
pip install -r requirements.txt
```

### 4\. Database Setup

This project uses SQLite, a file-based database. You need to create the database file and the hr\_contacts table within it, and populate it with your HR data.

#### a. Create the Database File and Table Manually (Recommended)

1.  **Download DB Browser for SQLite:** This is a free, visual tool that makes managing SQLite databases easy. Download from [sqlitebrowser.org/dl/](https://sqlitebrowser.org/dl/).
    
2.  **Create New Database:** Open DB Browser for SQLite. Go to File > New Database. Save the file as hr_emails.db in your project's root directory (the same folder as script.py).
    
3.  ```sql
    CREATE TABLE company_wise_hr_contacts ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, company TEXT, email TEXT UNIQUE, is_mail_sent INTEGER DEFAULT 0, last_sent_date TEXT);
    ```
    Click the "Execute SQL" button (usually a play icon).
    
4.  **Populate Data:** Go to the "Browse Data" tab. Select the company_wise_hr_contacts table from the dropdown. Use the "New Record" button to manually add your HR contact details (Name, Company, Email). Ensure is_mail_sent is set to 0 for all new contacts you want to send emails to.
    
5.  **Write Changes:** After adding data, click File > Write Changes (or the "Write Changes" icon) to save everything to your hr_emails.db file.
    

#### b. (Optional) Initial Data Import from CSV

If you have a large hrs.csv file, you could use a one-time Python script to import data into the hr_emails.db after creating the table._(Note: The main script.py script does NOT handle CSV import automatically; you'd use a separate utility script for that.)_

### 5\. Environment Variables Setup

Sensitive information is stored in environment variables, loaded from a .env file, which is kept out of version control.

#### a. Create .env File

In your project's root directory (the same folder as script.py), create a new file named **.env**.

#### b. Add Credentials to .env

Edit the .env file and add the following lines, replacing the placeholder values with your actual information:
```plain
SENDER_EMAIL="your_email@gmail.com" 
SENDER_PASSWORD="your_generated_app_password"  
RESUME_PATH="/path/to/your/resume.pdf" # e.g., "C:/Users/YourUser/Documents/MyResume.pdf" or "/home/user/Documents/MyResume.pdf"  
YOUR_FULL_NAME="Your Name"  
YOUR_PHONE_NUMBER="+91-1234567890" # Your contact number  
YOUR_LINKEDEDIN_URL="https://www.linkedin.com/in/yourprofile" # Your full LinkedIn URL  
  ```

**Important Notes for Credentials:**

*   **Gmail App Password:** If you are using a Gmail account with 2-Factor Authentication (2FA) enabled (which you should!), you cannot use your regular Gmail password. You must generate an **App Password**.
    
    *   Go to your Google Account.
        
    *   Navigate to Security > How you sign in to Google > App Passwords.
        
    *   Select "Mail" for the app and "Other (Custom name)" for the device. Give it a name like "HR Email Sender".
        
    *   Generate the password and use the 16-character code as your SENDER_PASSWORD.
        
*   **File Paths:** Ensure RESUME_PATH is the **absolute path** to your resume PDF file. Use forward slashes (/) even on Windows paths.
    
*   **Personalization:** YOUR_NAME, YOUR_PHONE_NUMBER, and YOUR_LINKEDIN_URL will be used to personalize the email body.
    

#### c. Update .gitignore

To prevent your sensitive .env file from being committed to Git, ensure your .gitignore file (also in the project's root directory) contains this line:

```plain
.env
```

If you don't have a .gitignore file, create one.

How to Run the Script
---------------------

Once all the setup steps are complete:

1.  **Activate your virtual environment** (if not already active):
    
    *   **On Windows:** .\\venv\\Scripts\\activate
        
    *   **On macOS/Linux:** source venv/bin/activate
        
2.  Bashpython script.py
    

The script will read from your hr_emails.db, send emails to unsent contacts (up to the daily limit), and update their status in the database.

### Daily Scheduling (Optional)

The script includes commented-out code for daily scheduling using the schedule library. If you want it to run automatically every day at a specific time:

1.  **Uncomment** the schedule.every().day.at(...) and while True: blocks at the bottom of script.py.
    
2.  **Adjust the time** ("09:00") to your desired daily sending time.
    
3.  **Keep your terminal/command prompt open and running** while the virtual environment is active. For a more robust solution that doesn't require keeping your computer on, consider using cloud-based scheduling services (e.g., AWS Lambda, Google Cloud Functions, or a dedicated server).
    

Customization
-------------

*   **Daily Email Limit:** Adjust the limit parameter in get_unsent_contacts(limit=100) within the automated_job_application_with_db function to control how many emails are sent per run.
    
*   **Email Content:** Modify the HTML body string within the create_email function to change the email's message, introduce more variables, or change bolded text.
    
*   **Delay:** Adjust time.sleep(5) within the main loop to increase or decrease the delay between sending each email. A longer delay reduces spam risk but slows down the process.

        

Disclaimer
----------

Be mindful of email sending limits (e.g., Gmail's 500 emails per 24 hours for free accounts, 2000 for Google Workspace). Sending large volumes of unsolicited emails can lead to your emails being marked as spam or your account being temporarily blocked. Always send professionally and respect recipients' privacy. This script is intended for legitimate job application outreach.
