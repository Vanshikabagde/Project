import json
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ml_predictor import predictor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/health_assessment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure instance folder is available for the database
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.context_processor
def inject_personal_info():
    if current_user.is_authenticated:
        personal_info = current_user.personal_info
        return {'personal_info': personal_info}
    return {}

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    personal_info = db.relationship('PersonalInfo', backref='user', uselist=False)
    assessments = db.relationship('Assessment', backref='user', lazy=True)

class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    bmi = db.Column(db.Float)
    blood_type = db.Column(db.String(10))
    smoking_status = db.Column(db.String(20))
    exercise_frequency = db.Column(db.String(50))
    family_history = db.Column(db.Text)
    medical_conditions = db.Column(db.Text)
    medications = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    risk_level = db.Column(db.String(20))
    risk_factors = db.Column(db.Text)  # JSON string
    recommendations = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions
def calculate_bmi(height, weight):
    if height and weight and height > 0:
        return round(weight / ((height / 100) ** 2), 1)
    return None

def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal weight'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

def assess_risk(assessment_data):
    """Assess risk using ML model with fallback"""
    try:
        # Prepare data for ML model
        ml_data = {
            'age': assessment_data.get('age', 0),
            'bmi': assessment_data.get('bmi', 25),  # Default BMI if not calculated
            'smoking_status': assessment_data.get('smoking_status', 'never'),
            'exercise_frequency': assessment_data.get('exercise_frequency', 'weekly'),
            'medical_conditions': assessment_data.get('medical_conditions', 0)
        }

        # Get ML prediction
        risk_level, confidence_scores = predictor.predict_risk(ml_data)

        # Create risk factors based on input data
        risk_factors = []

        if ml_data['age'] > 60:
            risk_factors.append('Age over 60')
        elif ml_data['age'] > 40:
            risk_factors.append('Age 40-60')

        if ml_data['bmi'] >= 30:
            risk_factors.append(f'BMI: {ml_data["bmi"]:.1f} (Obese)')
        elif ml_data['bmi'] >= 25:
            risk_factors.append(f'BMI: {ml_data["bmi"]:.1f} (Overweight)')
        elif ml_data['bmi'] < 18.5:
            risk_factors.append(f'BMI: {ml_data["bmi"]:.1f} (Underweight)')

        if ml_data['smoking_status'] == 'current':
            risk_factors.append('Current smoker')
        elif ml_data['smoking_status'] == 'former':
            risk_factors.append('Former smoker')

        if ml_data['exercise_frequency'] in ['never', 'rarely']:
            risk_factors.append('Low exercise frequency')

        if ml_data['family_history']:
            risk_factors.append('Family history of diseases')

        if ml_data['medical_conditions']:
            risk_factors.append('Existing medical conditions')

        if ml_data['medications']:
            risk_factors.append('Currently taking medications')

        return risk_level, risk_factors

    except Exception as e:
        print(f"ML prediction failed: {e}")
        # Fallback to rule-based system
        risk_level = 'Low'
        risk_factors = []

        # Age factor
        if assessment_data.get('age', 0) > 60:
            risk_level = 'High'
            risk_factors.append('Age over 60')
        elif assessment_data.get('age', 0) > 40:
            risk_level = 'Medium'
            risk_factors.append('Age 40-60')

        # BMI factor
        bmi = assessment_data.get('bmi')
        if bmi:
            if bmi >= 30:
                risk_level = 'High'
                risk_factors.append(f'BMI: {bmi} (Obese)')
            elif bmi >= 25:
                risk_level = 'Medium' if risk_level == 'Low' else 'High'
                risk_factors.append(f'BMI: {bmi} (Overweight)')

        # Other factors...
        if assessment_data.get('smoking_status') == 'current':
            risk_level = 'Medium' if risk_level == 'Low' else 'High'
            risk_factors.append('Current smoker')

        if assessment_data.get('exercise_frequency') in ['never', 'rarely']:
            risk_level = 'Medium' if risk_level == 'Low' else 'High'
            risk_factors.append('Low exercise frequency')

        if assessment_data.get('medical_conditions'):
            risk_level = 'High'
            risk_factors.append('Existing medical conditions')

        return risk_level, risk_factors

def generate_recommendations(risk_level, risk_factors):
    recommendations = [
        "Schedule regular check-ups with your healthcare provider",
        "Maintain a balanced diet rich in fruits and vegetables"
    ]

    if risk_level == 'High':
        recommendations.extend([
            "Consider consulting a specialist for comprehensive health screening",
            "Monitor your health indicators closely and keep records"
        ])

    if any('BMI' in factor for factor in risk_factors):
        recommendations.extend([
            "Focus on achieving and maintaining a healthy weight through diet and exercise",
            "Consider consulting a nutritionist for personalized dietary advice"
        ])

    if any('smoker' in factor.lower() for factor in risk_factors):
        recommendations.extend([
            "Consider smoking cessation programs - your doctor can help",
            "Avoid secondhand smoke and smoky environments"
        ])

    if any('exercise' in factor.lower() for factor in risk_factors):
        recommendations.extend([
            "Aim for at least 150 minutes of moderate exercise per week",
            "Find activities you enjoy - walking, swimming, or cycling"
        ])

    if any('Age' in factor for factor in risk_factors):
        recommendations.extend([
            "Age-related screenings become more important - discuss with your doctor",
            "Stay socially active and engaged for better mental health"
        ])

    if any('medical' in factor.lower() for factor in risk_factors):
        recommendations.extend([
            "Follow your treatment plan and medication schedule carefully",
            "Keep a health diary to track symptoms and medication effects"
        ])

    return recommendations

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    personal_info = current_user.personal_info
    recent_assessments = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).limit(5).all()

    return render_template('dashboard.html', personal_info=personal_info, assessments=recent_assessments)

@app.route('/personal-info', methods=['GET', 'POST'])
@login_required
def personal_info():
    personal_info = current_user.personal_info

    if request.method == 'POST':
        if not personal_info:
            personal_info = PersonalInfo(user_id=current_user.id)

        personal_info.first_name = request.form.get('first_name')
        personal_info.last_name = request.form.get('last_name')
        personal_info.phone = request.form.get('phone')
        personal_info.address = request.form.get('address')

        dob_str = request.form.get('date_of_birth')
        if dob_str:
            personal_info.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()

        personal_info.gender = request.form.get('gender')
        personal_info.emergency_contact = request.form.get('emergency_contact')
        personal_info.emergency_phone = request.form.get('emergency_phone')
        db.session.commit()
        flash('Personal information updated successfully!')
        return redirect(url_for('dashboard'))

    return render_template('personal_info.html', personal_info=personal_info)

@app.route('/assessment', methods=['GET', 'POST'])
@login_required
def assessment():
    personal_info = current_user.personal_info
    if not personal_info:
        flash('Please complete your personal information first.')
        return redirect(url_for('personal_info'))

    if request.method == 'POST':
        # Create new assessment
        assessment_data = {
            'age': int(request.form.get('age', 0)),
            'height': float(request.form.get('height', 0) or 0),
            'weight': float(request.form.get('weight', 0) or 0),
            'smoking_status': request.form.get('smoking_status'),
            'exercise_frequency': request.form.get('exercise_frequency'),
            'medical_conditions': int(request.form.get('medical_conditions', 0) or 0)
        }

        # Calculate BMI
        bmi = calculate_bmi(assessment_data['height'], assessment_data['weight'])
        assessment_data['bmi'] = bmi

        # Assess risk
        risk_level, risk_factors = assess_risk(assessment_data)

        # Generate recommendations
        recommendations = generate_recommendations(risk_level, risk_factors)

        # Save to database
        new_assessment = Assessment(
            user_id=current_user.id,
            **assessment_data,
            risk_level=risk_level,
            risk_factors=json.dumps(risk_factors),
            recommendations=json.dumps(recommendations)
        )

        db.session.add(new_assessment)
        db.session.commit()

        return render_template('assessment_result.html',
                             assessment=new_assessment,
                             risk_factors=risk_factors,
                             recommendations=recommendations,
                             bmi_category=get_bmi_category(bmi) if bmi else None)

    return render_template('assessment.html')

@app.route('/assessment/<int:assessment_id>')
@login_required
def assessment_result(assessment_id):
    assessment = Assessment.query.filter_by(id=assessment_id, user_id=current_user.id).first()
    if not assessment:
        flash('Assessment not found.')
        return redirect(url_for('dashboard'))

    risk_factors = json.loads(assessment.risk_factors) if assessment.risk_factors else []
    recommendations = json.loads(assessment.recommendations) if assessment.recommendations else []

    return render_template('assessment_result.html',
                         assessment=assessment,
                         risk_factors=risk_factors,
                         recommendations=recommendations,
                         bmi_category=get_bmi_category(assessment.bmi) if assessment.bmi else None)

@app.route('/history')
@login_required
def history():
    assessments = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).all()
    return render_template('history.html', assessments=assessments)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# API endpoints
@app.route('/api/bmi', methods=['POST'])
@login_required
def api_calculate_bmi():
    data = request.get_json()
    height = data.get('height', 0)
    weight = data.get('weight', 0)

    bmi = calculate_bmi(height, weight)
    category = get_bmi_category(bmi) if bmi else None

    return jsonify({
        'bmi': bmi,
        'category': category,
        'status': 'success' if bmi else 'error'
    })

@app.route('/api/progress', methods=['POST'])
@login_required
def api_form_progress():
    data = request.get_json()
    form_data = data.get('formData', {})

    required_fields = ['name', 'email', 'age', 'height', 'weight', 'smoking_status', 'exercise_frequency']
    optional_fields = ['blood_type', 'family_history', 'medical_conditions', 'medications', 'symptoms', 'bloodType', 'smokingStatus', 'exerciseFrequency']

    filled_required = sum(1 for field in required_fields if form_data.get(field))
    filled_optional = sum(1 for field in optional_fields if form_data.get(field))

    total_fields = len(required_fields) + len(optional_fields)
    filled_fields = filled_required + filled_optional
    progress_percent = (filled_fields / total_fields) * 100

    return jsonify({
        'progress': round(progress_percent, 1),
        'filled_required': filled_required,
        'total_required': len(required_fields),
        'filled_optional': filled_optional,
        'total_optional': len(optional_fields)
    })

@app.route('/statistics')
@login_required
def statistics():
    """Show health statistics and data insights"""
    stats = predictor.get_health_statistics()
    user_assessments = Assessment.query.filter_by(user_id=current_user.id).all()

    # Calculate user-specific statistics
    user_stats = {
        'total_assessments': len(user_assessments),
        'average_risk': None,
        'risk_distribution': {'Low': 0, 'Medium': 0, 'High': 0},
        'avg_bmi': None
    }

    if user_assessments:
        risk_levels = [a.risk_level for a in user_assessments]
        user_stats['risk_distribution'] = {
            'Low': risk_levels.count('Low'),
            'Medium': risk_levels.count('Medium'),
            'High': risk_levels.count('High')
        }

        # Calculate average BMI
        bmis = [a.bmi for a in user_assessments if a.bmi]
        if bmis:
            user_stats['avg_bmi'] = round(sum(bmis) / len(bmis), 1)

    return render_template('statistics.html', stats=stats, user_stats=user_stats)

@app.route('/api/statistics')
@login_required
def api_statistics():
    """API endpoint for statistics data"""
    stats = predictor.get_health_statistics()
    return jsonify(stats or {})

@app.route('/api/user-stats')
@login_required
def api_user_stats():
    """API endpoint for user-specific statistics"""
    assessments = Assessment.query.filter_by(user_id=current_user.id).all()

    data = {
        'total_assessments': len(assessments),
        'risk_trend': [],
        'bmi_trend': []
    }

    for assessment in assessments[-10:]:  # Last 10 assessments
        data['risk_trend'].append({
            'date': assessment.created_at.strftime('%Y-%m-%d'),
            'risk': assessment.risk_level
        })
        if assessment.bmi:
            data['bmi_trend'].append({
                'date': assessment.created_at.strftime('%Y-%m-%d'),
                'bmi': assessment.bmi
            })

    return jsonify(data)

@app.route('/api/feature-importance')
@login_required
def api_feature_importance():
    """API endpoint for feature importance data"""
    try:
        importance = predictor.get_feature_importance()
        # Sort by importance and format for display
        sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)
        return jsonify(sorted_features)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)