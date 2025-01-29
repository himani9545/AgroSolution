from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import os
import csv
from flask import jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import time

# Initialize the Flask app
app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/try')
def try_for_free():
    return render_template('try.html')  # Create a 'try.html' page for this route

@app.route('/signup', methods=['POST'])
def signup():
    # Get form data
    name = request.form.get('name')  # Matches 'name="name"' in HTML
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirmPassword')

    # Validate passwords match
    if password != confirm_password:
        return jsonify({"message": "Passwords do not match!"}), 400

    # Save data to a file (CSV format)
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, password])

    # Send welcome email after successful sign-up
    send_welcome_email(email, name)

    # Return a success response
    return jsonify({"message": "Sign up successful!"}), 200

def send_welcome_email(user_email, user_name):
    # Email credentials (use your own email and app password)
    sender_email = "vanditanandal07@gmail.com"
    sender_password = "rnis oopm bref mlmq"  # For Gmail, use an app-specific password

    # Create the email
    subject = "Welcome to Our Service"
    body = f"Hello {user_name},\n\nWelcome to AgroSolution! You can now login using your email: {user_email} and the password you set during registration.\n\nBest Regards,\nTeam AgroSolution"

    # Set up the email server
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, user_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

streamlit_started = False
@app.route('/run_streamlit_crop')
def run_streamlit_crop():
    global streamlit_started    
    return render_template('streamlit_iframe_crop.html')  # Redirect to the Streamlit app

@app.route('/run_streamlit_ferti')
def run_streamlit_ferti():
    global streamlit_started    
    return render_template('streamlit_iframe_ferti.html')

@app.route('/run_streamlit_pesticide')
def run_streamlit_pesticide():
    global streamlit_started    
    return render_template('streamlit_iframe_pesticide.html')


if __name__ == '__main__':
    app.run(debug=True)