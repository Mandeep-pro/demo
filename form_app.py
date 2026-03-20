"""
Professional Form Validation Web Application
Built with Flask and WTForms
"""

from flask import Flask, render_template, request, jsonify
from wtforms import StringField, EmailField, PasswordField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional, EqualTo
from flask_wtf import FlaskForm
import re
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'


class ContactForm(FlaskForm):
    """Form validation class using WTForms"""
    
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters'),
        Regexp(r'^[a-zA-Z\s]+$', message='First name can only contain letters')
    ])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters'),
        Regexp(r'^[a-zA-Z\s]+$', message='Last name can only contain letters')
    ])
    
    email = EmailField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(min=10, message='Phone number must be at least 10 characters'),
        Regexp(r'^[0-9+\-\s()]*$', message='Please enter a valid phone number')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    
    country = SelectField('Country', validators=[
        DataRequired(message='Please select a country')
    ], choices=[
        ('', 'Select a country'),
        ('usa', 'United States'),
        ('canada', 'Canada'),
        ('uk', 'United Kingdom'),
        ('india', 'India'),
        ('australia', 'Australia'),
        ('germany', 'Germany'),
        ('france', 'France'),
        ('japan', 'Japan'),
        ('other', 'Other')
    ])
    
    message = TextAreaField('Message', validators=[
        Optional(),
        Length(max=1000, message='Message cannot exceed 1000 characters')
    ])
    
    subscribe_newsletter = BooleanField('Subscribe to newsletter')
    
    agree_terms = BooleanField('I agree to terms and conditions', validators=[
        DataRequired(message='You must agree to terms and conditions')
    ])


def validate_password_strength(password):
    """
    Validate password strength
    Returns: dict with validation details
    """
    validation = {
        'has_uppercase': bool(re.search(r'[A-Z]', password)),
        'has_lowercase': bool(re.search(r'[a-z]', password)),
        'has_number': bool(re.search(r'\d', password)),
        'has_special': bool(re.search(r'[@$!%*?&]', password)),
        'min_length': len(password) >= 8
    }
    
    validation['is_strong'] = all(validation.values())
    validation['strength_score'] = sum(validation.values()) * 20  # 0-100
    
    return validation


@app.route('/')
def index():
    """Home page"""
    form = ContactForm()
    return render_template('index.html', form=form)


@app.route('/validate-password', methods=['POST'])
def validate_password():
    """AJAX endpoint for real-time password validation"""
    data = request.get_json()
    password = data.get('password', '')
    
    validation = validate_password_strength(password)
    
    return jsonify(validation)


@app.route('/submit-form', methods=['POST'])
def submit_form():
    """Handle form submission"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Form is valid, process the data
        form_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'country': form.country.data,
            'message': form.message.data,
            'subscribe_newsletter': form.subscribe_newsletter.data,
            'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Here you can save to database, send email, etc.
        print("Form Data:", form_data)
        
        return jsonify({
            'success': True,
            'message': 'Form submitted successfully!',
            'data': form_data
        })
    else:
        # Form has errors
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list[0]
        
        return jsonify({
            'success': False,
            'message': 'Form validation failed',
            'errors': errors
        }), 400


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/api/form-stats')
def form_stats():
    """API endpoint for form statistics"""
    stats = {
        'total_fields': 9,
        'required_fields': 7,
        'validation_types': [
            'String length',
            'Email format',
            'Password strength',
            'Pattern matching',
            'Field matching',
            'Dropdown selection'
        ],
        'supported_countries': 9
    }
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)