# HealthGuard - Complete Project Documentation
## AI-Powered Health Assessment Platform

---

# 📍 PART 1: WHERE DATA IS SAVED

## 1.1 Data Storage Location
- **Database Type:** SQLite
- **File Location:** `C:\Mini Project\instance\health_assessment.db`
- **Format:** Binary database file
- **Access:** Through SQLAlchemy ORM (Object-Relational Mapping)

## 1.2 Why SQLite?
✅ **Lightweight** - Single file database, no separate server needed
✅ **Perfect for development** - Built into Python
✅ **Portable** - Easy to share/backup
✅ **ACID Compliant** - Data integrity guaranteed

---

# 📊 PART 2: DATABASE STRUCTURE

## 2.1 Three Main Tables

### TABLE 1: User (Authentication)
```
USER TABLE STRUCTURE:
┌─────────────────────────────────────────────────────────┐
│ COLUMN NAME        │ TYPE           │ PURPOSE            │
├─────────────────────────────────────────────────────────┤
│ id                 │ Integer (PK)   │ Unique user ID     │
│ username           │ String(150)    │ Login username     │
│ email              │ String(150)    │ Email address      │
│ password_hash      │ String(128)    │ Encrypted password │
│ created_at         │ DateTime       │ Account creation   │
└─────────────────────────────────────────────────────────┘

Example Data:
id: 1
username: john_doe
email: john@example.com
password_hash: pbkdf2:sha256:260000$abc123xyz...
created_at: 2026-04-11 10:30:45
```

**Why password_hash?** 
- Raw passwords are NEVER stored
- Uses PBKDF2 encryption (secure hashing)
- Cannot be reversed, only verified

---

### TABLE 2: PersonalInfo (User Details)
```
PERSONALINFO TABLE STRUCTURE:
┌──────────────────────────────────────────────────────────┐
│ COLUMN NAME        │ TYPE           │ PURPOSE            │
├──────────────────────────────────────────────────────────┤
│ id                 │ Integer (PK)   │ Unique record ID   │
│ user_id (FK)       │ Integer        │ Links to User      │
│ first_name         │ String(100)    │ First name         │
│ last_name          │ String(100)    │ Last name          │
│ phone              │ String(20)     │ Contact number     │
│ address            │ Text           │ Home address       │
│ date_of_birth      │ Date           │ DOB for age calc   │
│ gender             │ String(20)     │ Male/Female/Other  │
│ emergency_contact  │ String(100)    │ Emergency name     │
│ emergency_phone    │ String(20)     │ Emergency number   │
│ created_at         │ DateTime       │ Record creation    │
│ updated_at         │ DateTime       │ Last modification  │
└──────────────────────────────────────────────────────────┘

Example Data:
id: 1
user_id: 1 (Links to User table)
first_name: John
last_name: Doe
phone: 9876543210
gender: Male
date_of_birth: 1990-05-15
emergency_contact: Jane Doe
emergency_phone: 9876543211
```

---

### TABLE 3: Assessment (Health Data & Results)
```
ASSESSMENT TABLE STRUCTURE:
┌────────────────────────────────────────────────────────────────┐
│ COLUMN NAME         │ TYPE          │ PURPOSE                   │
├────────────────────────────────────────────────────────────────┤
│ id                  │ Integer (PK)  │ Unique assessment ID      │
│ user_id (FK)        │ Integer       │ Links to User             │
│ age                 │ Integer       │ User age                  │
│ height              │ Float         │ Height in cm              │
│ weight              │ Float         │ Weight in kg              │
│ bmi                 │ Float         │ Calculated BMI            │
│ blood_type          │ String(10)    │ A/B/O/AB etc              │
│ smoking_status      │ String(20)    │ never/former/current      │
│ exercise_frequency  │ String(50)    │ daily/weekly/monthly etc  │
│ family_history      │ Text          │ Health conditions in family
│ medical_conditions  │ Text          │ User's existing conditions│
│ medications         │ Text          │ Current medications      │
│ symptoms            │ Text          │ Reported symptoms        │
│ risk_level          │ String(20)    │ Low/Medium/High           │
│ risk_factors        │ Text (JSON)   │ Individual risk factors   │
│ recommendations     │ Text (JSON)   │ Health recommendations   │
│ created_at          │ DateTime      │ Assessment date           │
└────────────────────────────────────────────────────────────────┘

Example Data:
id: 1
user_id: 1
age: 35
height: 180
weight: 75
bmi: 23.1
smoking_status: never
exercise_frequency: weekly
risk_level: Low
risk_factors: ["Age between 30-40", "BMI in normal range"]
recommendations: ["Continue regular exercise", "Maintain healthy diet"]
```

## 2.2 Data Relationships (Foreign Keys)
```
      USER TABLE (Parent)
           ↓
      ┌────┴────┐
      ↓         ↓
 PersonalInfo  Assessment
 (1:1)         (1:Many)

One User can have:
- One PersonalInfo record (basic details)
- Multiple Assessment records (history of assessments)
```

---

# 🔄 PART 3: HOW DATA FLOWS THROUGH THE APPLICATION

## 3.1 User Registration Flow

```
USER REGISTRATION:
┌─────────────┐
│  User Input │──── Username, Email, Password
└──────┬──────┘
       ↓
┌──────────────────────────┐
│ Validation Check         │──── Check if username exists
│ Backend: app.py          │     Check if email exists
└──────┬───────────────────┘
       ↓ (If valid)
┌──────────────────────────┐
│ Password Hashing         │──── Convert password to hash
│ werkzeug.security        │     (md5, sha256 encryption)
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ Database INSERT          │──── INSERT into User table
│ SQLAlchemy ORM           │     id, username, email, password_hash
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ User Created ✓           │──── Session created
│ Redirect to Dashboard    │     User logged in
└──────────────────────────┘
```

**Code Example:**
```python
# In app.py
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return "Username already exists"
    
    # Hash password (not stored as plain text!)
    password_hash = generate_password_hash(password)
    
    # Create new user
    new_user = User(username=username, email=email, password_hash=password_hash)
    
    # Save to database
    db.session.add(new_user)
    db.session.commit()
```

---

## 3.2 Login Flow

```
USER LOGIN:
┌─────────────────────┐
│ Input Credentials   │──── Username & Password
└──────┬──────────────┘
       ↓
┌──────────────────────────────┐
│ Query User from Database     │──── SELECT * FROM User WHERE username=?
│ SQLAlchemy: User.query       │
└──────┬───────────────────────┘
       ↓
       ├─→ User NOT found? ❌─→ "Invalid credentials"
       │
       └─→ User found? ✓
              ↓
         ┌────────────────────────┐
         │ Verify Password        │──── Compare password hash
         │ check_password_hash()  │
         └────┬───────────────────┘
              ↓
              ├─→ Password wrong? ❌─→ "Invalid credentials"
              │
              └─→ Password correct? ✓
                     ↓
                ┌────────────────────┐
                │ Create Session     │──── User logged in
                │ Flask-Login        │
                └────┬───────────────┘
                     ↓
                ┌────────────────────┐
                │ Redirect Dashboard │
                └────────────────────┘
```

---

## 3.3 Personal Information Filing Flow

```
PERSONAL INFO FORM SUBMISSION:
┌──────────────────────────────────┐
│ User Fills Form                  │
│ - First Name, Last Name          │
│ - Phone, Address                 │
│ - Date of Birth, Gender          │
│ - Emergency Contact              │
└──────┬───────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Frontend Validation (HTML5)      │──── Check required fields
│ JavaScript (optional)            │     Validate phone format
└──────┬───────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Backend Processing               │──── Check if PersonalInfo exists
│ app.py: personal_info()          │
└──────┬───────────────────────────┘
       ↓
       ├─→ If PersonalInfo exists? UPDATE record
       │
       └─→ If NOT exists? CREATE new record
              ↓
         ┌────────────────────────┐
         │ INSERT/UPDATE Database │
         │ PersonalInfo Table     │
         └────┬───────────────────┘
              ↓
         ┌────────────────────────┐
         │ Data Saved ✓           │──── Success message
         │ Redirect Dashboard     │
         └────────────────────────┘
```

**Stored Data Example:**
```
PersonalInfo Table:
id: 1
user_id: 1 <- Links to the logged-in user
first_name: "John"
last_name: "Doe"
phone: "9876543210"
date_of_birth: "1990-05-15"
```

---

## 3.4 Health Assessment Flow (Most Important!)

```
HEALTH ASSESSMENT FORM SUBMISSION:
┌───────────────────────────────────┐
│ User Fills Health Form            │
│ - Age, Height, Weight             │
│ - Blood Type, Smoking Status      │
│ - Exercise Frequency              │
│ - Family History                  │
│ - Medical Conditions              │
│ - Medications, Symptoms           │
└──────┬────────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Calculate BMI (Backend)          │──── BMI = weight / (height/100)²
│ Formula: Python function         │     Example: 75 / (1.8)² = 23.1
└──────┬───────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Prepare ML Model Input           │──── age: 35
│ Dict with all features           │     bmi: 23.1
│                                  │     smoking: 'never'
└──────┬───────────────────────────┘      exercise: 'weekly'
       ↓                                   family_history: 1
┌──────────────────────────────────────────────────────┐
│ ML MODEL PREDICTION (ml_predictor.py)               │
│                                                      │
│ RandomForestClassifier (Scikit-learn)              │
│ - Trained on 1000 sample health records            │
│ - Uses 7 features for prediction                   │
│ - Output: Risk Level & Confidence Scores           │
└──────┬───────────────────────────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ ML Output:                       │──── risk_level: "Low"
│ - Risk Level (Low/Medium/High)   │     confidence: 0.92 (92%)
│ - Confidence Score               │     OR
└──────┬───────────────────────────┘      risk_level: "High"
       ↓                                   confidence: 0.87 (87%)
┌──────────────────────────────────┐
│ Identify Risk Factors            │──── "Age: 35"
│ Based on user input              │     "BMI: 23.1 (Normal)"
│ Generate personalized factors    │     "Smoking: Never"
└──────┬───────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Generate Recommendations         │──── "Continue exercise"
│ Based on risk factors            │     "Maintain diet"
│ Health tips & advice             │     "Annual checkup"
└──────┬───────────────────────────┘
       ↓
┌──────────────────────────────────────────────────────┐
│ SAVE TO DATABASE (Assessment Table)                 │
│ INSERT INTO Assessment:                             │
│ - user_id: 1                                        │
│ - age, height, weight, bmi                          │
│ - smoking_status, exercise_frequency                │
│ - family_history, medical_conditions, medications   │
│ - risk_level: "Low"                                 │
│ - risk_factors: JSON string                         │
│ - recommendations: JSON string                      │
│ - created_at: 2026-04-11 15:30:45                  │
└──────┬───────────────────────────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Display Results to User          │──── Show risk level
│ Render assessment_result.html    │     Show risk factors
│ With charts & recommendations    │     Show recommendations
└──────────────────────────────────┘
```

**Python Code:**
```python
@app.route('/assessment', methods=['POST'])
def assessment():
    # 1. Get form data
    age = int(request.form.get('age'))
    height = float(request.form.get('height'))
    weight = float(request.form.get('weight'))
    
    # 2. Calculate BMI
    bmi = calculate_bmi(height, weight)
    
    # 3. Prepare ML input
    ml_data = {
        'age': age,
        'bmi': bmi,
        'smoking_status': request.form.get('smoking_status'),
        'exercise_frequency': request.form.get('exercise_frequency'),
        'family_history': 1 if request.form.get('family_history') else 0,
        'medical_conditions': 1 if request.form.get('medical_conditions') else 0,
        'medications': 1 if request.form.get('medications') else 0
    }
    
    # 4. Get ML prediction
    risk_level, confidence = predictor.predict_risk(ml_data)
    
    # 5. Create risk factors list
    risk_factors = [...]  # Generated based on input
    
    # 6. Generate recommendations
    recommendations = [...]  # Generated based on risk
    
    # 7. Save to database
    assessment = Assessment(
        user_id=current_user.id,
        age=age,
        height=height,
        weight=weight,
        bmi=bmi,
        risk_level=risk_level,
        risk_factors=json.dumps(risk_factors),
        recommendations=json.dumps(recommendations),
        created_at=datetime.utcnow()
    )
    db.session.add(assessment)
    db.session.commit()
    
    # 8. Render result page
    return render_template('assessment_result.html', assessment=assessment)
```

---

# 🤖 PART 4: MACHINE LEARNING MODEL

## 4.1 Model Details

**Model Type:** RandomForestClassifier (Supervised Learning)
**Framework:** scikit-learn
**Training Data:** 1000 synthetic health records
**Features Used:** 7 input variables
**Output:** Binary/Ternary classification (Low/Medium/High Risk)

## 4.2 ML Pipeline

```
TRAINING PHASE (ml_predictor.py):
┌─────────────────────────────┐
│ 1. Create Sample Dataset    │──── Generate 1000 records
│    (if not exists)          │     Realistic health data
└──────┬──────────────────────┘
       ↓
┌─────────────────────────────┐
│ 2. Encode Categorical Data  │──── smoking_status: 'never'→0
│    (Numeric conversion)     │     'former'→1, 'current'→2
└──────┬──────────────────────┘
       ↓
┌─────────────────────────────┐
│ 3. Scale Features           │──── Normalize to 0-1 range
│    (StandardScaler)         │     Important for accuracy
└──────┬──────────────────────┘
       ↓
┌─────────────────────────────┐
│ 4. Train/Test Split        │──── 80% training
│    (80-20 split)            │     20% validation
└──────┬──────────────────────┘
       ↓
┌─────────────────────────────┐
│ 5. Train RandomForest       │──── 100 decision trees
│    Model                    │     Bootstrap aggregating
└──────┬──────────────────────┘
       ↓
┌─────────────────────────────┐
│ 6. Evaluate Model           │──── Accuracy: ~85-95%
│    Classification Report    │     Precision, Recall, F1
└──────┬──────────────────────┘
       ↓
┌─────────────────────────────┐
│ 7. Save Model               │──── health_risk_model.pkl
│    (Binary serialization)   │     Joblib format
└─────────────────────────────┘
```

## 4.3 Prediction Process

```
PREDICTION PHASE (During Assessment):

Input Features:
┌────────────────────────────┐
│ age: 35                    │
│ bmi: 23.1                  │
│ smoking_status: 'never'→0  │
│ exercise_frequency: 'weekly'→3
│ family_history: 1          │
│ medical_conditions: 0      │
│ medications: 1             │
└────────┬───────────────────┘
         ↓
    ┌────────────┐
    │ 100 Trees  │
    │ (Ensemble) │
    └─┬──┬──┬────┘
      │  │  │ ...
      ↓  ↓  ↓
    Tree1 Tree2 Tree3  ...  Tree100
    "Low" "Low" "Low"       "Low"
      ↓  ↓  ↓
      └──┴──┴───────→ MAJORITY VOTE
                      95 voted "Low"
                      5 voted "Medium"
                      ↓
                   RESULT: "Low"
                   Confidence: 95/100 = 0.95
```

## 4.4 Feature Importance

```
RANDOM FOREST FEATURE IMPORTANCE:
(Which factors matter most)

1. age ==================== 25% importance
2. bmi ==================== 23% importance
3. smoking_status ========== 20% importance
4. exercise_frequency ====== 15% importance
5. medical_conditions ====== 10% importance
6. family_history ========== 5% importance
7. medications ============= 2% importance

This means:
- Age is most important for predicting risk
- BMI is second most important
- Medications matter least
```

---

# 🎨 PART 5: FRONTEND ARCHITECTURE

## 5.1 File Structure

```
Frontend Components:
templates/
├── base.html              (Base layout - shared)
├── index.html             (Landing page)
├── login.html             (User login form)
├── register.html          (User registration form)
├── dashboard.html         (User dashboard)
├── personal_info.html     (Personal details form)
├── assessment.html        (Health assessment form)
├── assessment_result.html (Results display)
├── history.html           (Assessment history)
└── statistics.html        (Analytics/graphs)

static/
├── css/
│   ├── enhanced_styles.css    (Main modern CSS)
│   ├── modern_styles.css      (Additional styles)
│   └── styles.css             (Legacy styles)
├── js/
│   └── main.js            (JavaScript logic)
└── data/
    └── sample_health_data.csv
```

## 5.2 HTML Templates (Jinja2)

**Jinja2:** Python templating engine
**Purpose:** Dynamic HTML generation

```html
<!-- Example: Jinja2 syntax -->
{% extends "base.html" %}         <!-- Inherit base template -->
{% block content %}                <!-- Insert content here -->
    <h1>Hello, {{ current_user.username }}!</h1>  <!-- Variables -->
    
    {% if assessments %}           <!-- Conditional -->
        {% for assessment in assessments %}
            <p>{{ assessment.created_at }}</p>    <!-- Loop -->
        {% endfor %}
    {% else %}
        <p>No assessments yet</p>
    {% endif %}
{% endblock %}
```

## 5.3 CSS - Modern Glassmorphism Design

```css
Key CSS Features:
- CSS Variables for consistent theming
- Gradient backgrounds
- Backdrop blur effects (modern look)
- Responsive grid layout
- Smooth transitions & animations
- Media queries for mobile/tablet/desktop
```

## 5.4 Form Validation

```
Frontend Validation (HTML5):
- required: Field must be filled
- type="email": Must be valid email format
- type="number": Only numbers allowed
- min/max attributes: Range checking

Backend Validation (Python):
- Check if username already exists
- Verify password requirements
- Validate email format
- Sanitize inputs (prevent SQL injection)
```

---

# ⚙️ PART 6: BACKEND ARCHITECTURE

## 6.1 Flask Framework

```python
## What is Flask?
- Lightweight Python web framework
- Uses Jinja2 for templating
- Built-in development server
- RESTful routing

## Basic Structure:
from flask import Flask, render_template, request

app = Flask(__name__)  # Create Flask app instance

@app.route('/path', methods=['GET', 'POST'])  # URL routing
def function_name():
    # Handle request
    return "Response"
```

## 6.2 Main Routes (Endpoints)

```
URL ROUTING:

GET  http://127.0.0.1:5000/              → index.html (Landing)
GET  http://127.0.0.1:5000/login         → login.html 
POST http://127.0.0.1:5000/login         → Process login
GET  http://127.0.0.1:5000/register      → register.html
POST http://127.0.0.1:5000/register      → Process registration
GET  http://127.0.0.1:5000/dashboard     → dashboard.html (Protected)
GET  http://127.0.0.1:5000/personal-info → personal_info.html
POST http://127.0.0.1:5000/personal-info → Save personal info
GET  http://127.0.0.1:5000/assessment    → assessment.html
POST http://127.0.0.1:5000/assessment    → Process & save assessment
GET  http://127.0.0.1:5000/history       → history.html (Show all assessments)
GET  http://127.0.0.1:5000/statistics    → statistics.html (Analytics)
```

## 6.3 Request-Response Cycle

```
COMPLETE HTTP CYCLE:

1. USER SUBMITS FORM
   └─→ Browser sends POST request
       Content: form data (name, value pairs)

2. SERVER RECEIVES REQUEST
   └─→ Flask routes to correct handler
       @app.route('/assessment', methods=['POST'])
       def assessment():

3. BACKEND PROCESSING
   └─→ Extract data: request.form.get('field_name')
   └─→ Validate data
   └─→ Process logic (calculate, predict)
   └─→ Save to database
   └─→ Query database if needed

4. GENERATE RESPONSE
   └─→ Render template: render_template('result.html', data=value)
   └─→ Pass data to template

5. SEND RESPONSE TO BROWSER
   └─→ HTML + CSS + JavaScript
   └─→ Browser renders page

6. USER SEES RESULT
   └─→ Dynamic page with their data displayed
```

---

# 🔐 PART 7: SECURITY & AUTHENTICATION

## 7.1 User Authentication (Flask-Login)

```
LOGIN SESSION MANAGEMENT:

Session = Temporary storage during login

Step 1: User logs in
    └─→ Credentials verified
    └─→ Session created in memory
    └─→ Session ID sent to browser (cookie)

Step 2: User browses website
    └─→ Browser automatically sends session ID in each request
    └─→ Server checks: "Is this session valid?"
    └─→ If valid: Allow access
    └─→ If invalid: Redirect to login

Step 3: User logs out
    └─→ Session destroyed
    └─→ Cookie deleted
    └─→ Must login again to access
```

## 7.2 Password Security

```
PASSWORD STORAGE (NOT in plain text!):

Plain password: "MyPassword123"
                    ↓
        Hash function (PBKDF2-SHA256)
                    ↓
Hash stored: pbkdf2:sha256:260000$SaltValueABC123$HashValueXYZ123

Why this matters:
✓ Even database hacked = passwords safe
✓ Can't decrypt hash (one-way function)
✓ Salt added = Rainbow table attack prevented
✓ 260,000 rounds = Brute force attack slowed

Login Verification:
User enters password → Hash it with same salt → Compare to stored hash
Match? → Login successful
```

## 7.3 Protected Routes

```python
# Routes requiring login:
@app.route('/dashboard')
@login_required  # Decorator: checks if user logged in
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # Only logged-in users reach here
```

---

# 📁 PART 8: COMPLETE FILE STRUCTURE EXPLAINED

```
C:\Mini Project\
│
├── app.py ⭐ MAIN APPLICATION FILE
│   ├── Flask app initialization
│   ├── Database models (User, PersonalInfo, Assessment)
│   ├── All route handlers (@app.route)
│   ├── Authentication logic
│   ├── Business logic (BMI calc, risk assessment)
│   └── Database operations
│
├── ml_predictor.py ⭐ MACHINE LEARNING MODEL
│   ├── HealthRiskPredictor class
│   ├── Data generation
│   ├── Model training & evaluation
│   ├── Prediction method
│   └── Saves model.pkl
│
├── wsgi.py
│   └── Production deployment configuration
│
├── requirements.txt
│   └── All Python dependencies with versions
│
├── instance/
│   └── health_assessment.db ⭐ SQLITE DATABASE
│       ├── User table
│       ├── PersonalInfo table
│       └── Assessment table
│
├── templates/ (HTML files - Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── personal_info.html
│   ├── assessment.html
│   ├── assessment_result.html
│   ├── history.html
│   └── statistics.html
│
├── static/ (Frontend assets)
│   ├── css/
│   │   ├── enhanced_styles.css (MAIN - Glassmorphism, gradients)
│   │   ├── modern_styles.css
│   │   └── styles.css
│   ├── js/
│   │   └── main.js (Form validation, interactions)
│   └── data/
│       └── sample_health_data.csv
│
├── README.md
├── SHARE_README.md
├── PROJECT_DOCUMENTATION.md (This file)
├── setup.py
├── ngrok.exe (For public sharing)
├── run_server.bat (Easy startup script)
└── get_network_info.bat (Show IP address)
```

---

# 🔄 PART 9: COMPLETE DATA FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────┐
│                    USER PERSPECTIVE                      │
│  1. Opens browser: http://127.0.0.1:5000/register      │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│                FRONTEND HTML/CSS/JS                     │
│  - Render registration form                            │
│  - Validate inputs (HTML5 + JavaScript)               │
│  - Send data to backend (POST request)                │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│              FLASK BACKEND (app.py)                     │
│  @app.route('/register', methods=['POST'])            │
│  - Extract form data                                   │
│  - Check username uniqueness (QUERY User table)       │
│  - Hash password (werkzeug.security)                  │
│  - Create User object                                 │
│  - db.session.add() & db.session.commit()             │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│           DATABASE (SQLite - health_assessment.db)     │
│  INSERT INTO User (id, username, email, password_hash)│
│  VALUES (1, 'john_doe', 'john@email.com', 'hash...'  │
│                                                       │
│  Result: New row created in User table               │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│              FLASK RESPONSE                            │
│  - Success message                                     │
│  - Redirect to login or dashboard                     │
│  - Send HTML response to browser                      │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│             BROWSER DISPLAY                            │
│  - User sees success message                          │
│  - Redirected to new page                             │
│  - User data now in database ✓                        │
└─────────────────────────────────────────────────────────┘
```

---

# 📊 PART 10: ASSESSMENT DATA EXAMPLE

```
Suppose user "John" takes an assessment:

INPUT (User fills form):
- Age: 35
- Height: 180 cm
- Weight: 75 kg
- Blood type: O+
- Smoking: Never
- Exercise: Weekly (3-4 days)
- Family history: Diabetes (mother)
- Medical conditions: None
- Medications: None
- Symptoms: Occasional fatigue

PROCESSING:
┌─ Calculate BMI:
│  BMI = 75 / (1.8)² = 23.1 (Normal)
│
├─ Prepare ML Input:
│  {
│    'age': 35,
│    'bmi': 23.1,
│    'smoking_status': 0,  # never=0
│    'exercise_frequency': 3,  # weekly=3
│    'family_history': 1,  # has history
│    'medical_conditions': 0,
│    'medications': 0
│  }
│
├─ ML Model Prediction:
│  100 decision trees vote → 92 say "Low", 8 say "Medium"
│  Result: "Low Risk" (92% confidence)
│
├─ Risk Factors Identified:
│  [
│    "Age: 35 (within healthy range)",
│    "BMI: 23.1 (Normal weight)",
│    "Regular exercise (weekly)",
│    "Non-smoker",
│    "Family history of diabetes - requires monitoring"
│  ]
│
└─ Generate Recommendations:
   [
     "Continue your weekly exercise routine",
     "Maintain balanced diet rich in vegetables",
     "Monitor blood sugar levels annually",
     "Get regular health checkups",
     "Manage family history of diabetes with lifestyle",
     "Aim for 7-8 hours of sleep daily"
   ]

SAVING TO DATABASE:
INSERT INTO Assessment (
  user_id=1,
  age=35,
  height=180,
  weight=75,
  bmi=23.1,
  smoking_status='never',
  exercise_frequency='weekly',
  family_history='Diabetes in mother',
  risk_level='Low',
  risk_factors='["Age: 35...", "BMI: 23.1...", ...]',
  recommendations='["Continue exercise...", ...]',
  created_at='2026-04-11 15:30:45'
);

OUTPUT (User sees):
┌─────────────────────────────────┐
│    Your Health Assessment       │
│                                 │
│    Risk Level: LOW ✓           │
│    Confidence: 92%              │
│                                 │
│    Key Factors:                 │
│    • Normal BMI (23.1)          │
│    • Regular exercise           │
│    • Non-smoker                 │
│    • Family risk: Monitor       │
│                                 │
│    Recommendations:             │
│    1. Continue weekly exercise  │
│    2. Balanced diet             │
│    3. Annual blood work         │
│    ...                          │
└─────────────────────────────────┘
```

---

# 🎓 PART 11: TECHNOLOGY STACK SUMMARY

```
FRONTEND:
├── HTML5 (Structure)
├── CSS3 (Glassmorphism, gradients, animations)
├── JavaScript (Form validation, interactions)
└── Bootstrap Icons (UI elements)

BACKEND:
├── Python 3.8+
├── Flask (Web framework)
├── Flask-SQLAlchemy (ORM)
├── Flask-Login (Authentication)
├── Werkzeug (Security - password hashing)
└── Jinja2 (Templating)

DATABASE:
├── SQLite (File-based)
├── SQLAlchemy (ORM - Object mapping)
└── Three tables (User, PersonalInfo, Assessment)

MACHINE LEARNING:
├── scikit-learn (ML library)
├── RandomForestClassifier (Model type)
├── pandas (Data manipulation)
├── numpy (Numerical computing)
└── joblib (Model serialization)

DEPLOYMENT:
├── ngrok (Public URL tunneling)
├── Flask dev server (Testing)
└── WSGI (Production deployment ready)
```

---

# 💾 PART 12: DATA PERSISTENCE

## How Data Survives Application Restarts:

```
Scenario: User registers, then app crashes

BEFORE CRASH:
User fills registration form
    ↓
Backend validates
    ↓
db.session.add(new_user)
db.session.commit() ← ⭐ CRITICAL: Writes to disk
    ↓
Data written to health_assessment.db file

APP CRASHES! 💥

AFTER RESTART:
App starts
    ↓
health_assessment.db file still exists on disk
    ↓
SQLAlchemy re-connects to database
    ↓
SELECT * FROM User returns all previous users
    ↓
User can login with credentials → LOGIN WORKS ✓

Why?
- Database file saved to: C:\Mini Project\instance\health_assessment.db
- Even if app crashes, file remains
- When app restarts, it reads the file
- All data is preserved
```

---

# 🔍 PART 13: TYPICAL INTERVIEW QUESTIONS & ANSWERS

**Q1: Where is the data stored?**
A: "Data is stored in SQLite database file located at `C:\Mini Project\instance\health_assessment.db`. We use SQLAlchemy ORM to interact with three tables: User (authentication), PersonalInfo (user details), and Assessment (health data & results)."

**Q2: How is password security handled?**
A: "Passwords are never stored as plain text. We use werkzeug.security to hash passwords using PBKDF2-SHA256 with salt. When user logs in, we hash the entered password and compare it to the stored hash."

**Q3: How does the ML model work?**
A: "We use RandomForestClassifier from scikit-learn. The model is trained on 1000 synthetic health records with 7 features (age, BMI, smoking, exercise, etc.). During assessment, all 100 trees in the forest predict, and we use majority voting for the final risk level."

**Q4: Explain the data flow for an assessment.**
A: "User fills health form → Frontend validates → Backend calculates BMI → Sends data to ML model → Model predicts risk level → Generate risk factors & recommendations → Save all data to Assessment table → Display results with insights."

**Q5: How is user authentication handled?**
A: "We use Flask-Login extension. When user logs in successfully, a session is created stored on server. Session ID is sent to browser as a cookie. Each request includes session cookie, which server validates. @login_required decorator protects routes."

---

# 📈 PART 14: KEY FILES TO SHOW EXAMINER

When presenting to examiner, highlight:

1. **app.py** - Show database models, routes, business logic
2. **ml_predictor.py** - Show model training and prediction
3. **templates/assessment.html** - Show form structure
4. **templates/assessment_result.html** - Show results display
5. **static/css/enhanced_styles.css** - Show modern UI design
6. **health_assessment.db** - Show actual database file

---

# 🚀 DEPLOYMENT & SHARING

**Local Access:**
```
http://127.0.0.1:5000 (localhost only)
http://192.168.31.87:5000 (network access)
```

**Global Access (ngrok):**
```
./ngrok http 5000
Output: https://abcd1234.ngrok.io (publicly accessible)
```

**Production Deployment:**
```
Heroku, PythonAnywhere, or cloud platforms
Use production WSGI server (Gunicorn, uWSGI)
```

---

# ✅ ADVANTAGES OF THIS ARCHITECTURE

1. **Modularity** - Separate concerns (Frontend, Backend, ML)
2. **Scalability** - Can add more routes, assessments, features
3. **Security** - Password hashing, session management, input validation
4. **Database** - ACID compliance, relationships, data integrity
5. **ML Integration** - Intelligent predictions, not hardcoded rules
6. **User Experience** - Modern responsive design, smooth interactions
7. **Maintainability** - Clear code structure, documentation

---

**END OF DOCUMENTATION**

This covers everything about the project! Good luck with your examination! 🎓
