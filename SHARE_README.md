# HealthGuard - AI-Powered Health Assessment Platform

A modern web application for health risk assessment using machine learning and AI-powered predictions.

## 🌐 Making Your Website Shareable

### Option 1: Local Network Access (Quick & Easy)

1. **Run the server:**
   ```bash
   python app.py
   ```
   Or use the provided batch file:
   ```bash
   run_server.bat
   ```

2. **Find your IP address:**
   - Open Command Prompt and run: `ipconfig`
   - Look for your IPv4 Address (e.g., 192.168.1.100)

3. **Share the URL:**
   - Local access: `http://127.0.0.1:5000`
   - Network access: `http://[YOUR_IP_ADDRESS]:5000`

### Option 2: Public Internet Access (Using ngrok)

1. **Install ngrok:**
   - Download from: https://ngrok.com/download
   - Create a free account
   - Follow installation instructions

2. **Run your Flask app:**
   ```bash
   python app.py
   ```

3. **Create public tunnel:**
   ```bash
   ngrok http 5000
   ```

4. **Share the generated HTTPS URL:**
   - ngrok will provide a URL like: `https://abc123.ngrok.io`
   - This URL is publicly accessible from anywhere

### Option 3: Deploy to Cloud (Recommended for Production)

#### Heroku Deployment:
1. Create a Heroku account
2. Install Heroku CLI
3. Initialize git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
4. Create Heroku app:
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

#### PythonAnywhere Deployment:
1. Create PythonAnywhere account
2. Upload your files
3. Configure web app settings
4. Set up virtual environment with requirements.txt

## 🚀 Features

- **AI-Powered Health Assessment** - Machine learning predictions
- **User Authentication** - Secure login/registration
- **Personal Health Dashboard** - Track your health metrics
- **Risk Analysis** - Comprehensive health risk evaluation
- **Modern UI** - Responsive design with glassmorphism effects
- **Data Visualization** - Charts and analytics
- **Secure Database** - SQLite with SQLAlchemy ORM

## 📋 Requirements

- Python 3.8+
- Flask
- scikit-learn
- SQLAlchemy
- Flask-Login

## 🛠️ Installation

1. Clone/download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## 🔒 Security Notes

- Change the SECRET_KEY in production
- Use environment variables for sensitive data
- Consider using PostgreSQL for production database
- Enable HTTPS in production

## 📞 Support

For questions or issues, please check the code comments or create an issue in the repository.