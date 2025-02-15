from flask import Flask, request, render_template, redirect, url_for, jsonify, make_response
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from data import crops_data, crops_data_hindi  # Import both dictionaries

# Initialize the Flask app
app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    # Get language preference from cookies (default is 'en')
    language = request.cookies.get('language', 'en')
    return render_template('home.html', language=language)

@app.route('/set_language/<lang>')
def set_language(lang):
    """Set the language preference in cookies and refresh the page."""
    if lang not in ['en', 'hi']:
        return redirect(url_for('home'))  # If invalid language, go to home
    
    response = make_response(redirect(request.referrer or url_for('home')))
    response.set_cookie('language', lang, max_age=30*24*60*60)  # Save for 30 days
    return response

@app.route('/try')
def try_for_free():
    return render_template('try.html')

@app.route('/crops')
def crops():
    language = request.cookies.get('language', 'en')
    return render_template('crops.html', language=language)

@app.route('/crop_info')
def crop_info():
    crop_name = request.args.get('crop')  # Get crop name from query parameter
    if not crop_name:
        return redirect(url_for('home'))  # Redirect to homepage if invalid crop
    
    language = request.cookies.get('language', 'en')  # Get language preference

    # Fetch description from the correct dictionary based on language preference
    if language == 'hi':
        crop_description = crops_data_hindi.get(crop_name, {}).get("description", "⚠ विवरण उपलब्ध नहीं है")
    else:
        crop_description = crops_data.get(crop_name, {}).get("description", "⚠ Description not available")

    # Ensure the description is formatted correctly for HTML
    crop_description = crop_description.replace('\n', '<br>')

    # Generate crop image filename dynamically
    crop_image = crop_name.lower().replace(" ", "") + "1.jpg"

    return render_template('crop_info.html', 
                           crop_name=crop_name.capitalize(),
                           crop_description=crop_description, 
                           crop_image=crop_image,
                           language=language)

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirmPassword')

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match!"}), 400

    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, password])

    send_welcome_email(email, name)

    return jsonify({"message": "Sign up successful!"}), 200

def send_welcome_email(user_email, user_name):
    sender_email = "agrosolutiontech@gmail.com"
    sender_password = "wiav aegh oanu jwxh "  # Use app-specific password

    subject = "Welcome to AgroSolution"
    body = f"Hello {user_name},\n\nWelcome to AgroSolution! You can now login using your email: {user_email} and the password you set during registration.\n\nBest Regards,\nTeam AgroSolution"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

# Routes to run Streamlit apps
@app.route('/run_streamlit_crop')
def run_streamlit_crop():
    return render_template('streamlit_iframe_crop.html')

@app.route('/run_streamlit_ferti')
def run_streamlit_ferti():
    return render_template('streamlit_iframe_ferti.html')

@app.route('/run_streamlit_pesticide')
def run_streamlit_pesticide():
    return render_template('streamlit_iframe_pesticide.html')

@app.route('/about')
def about():
    language = request.cookies.get('language', 'en')
    return render_template('about.html', language=language)

if __name__ == '__main__':
    app.run(debug=True)
