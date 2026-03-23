# AWS Elastic Beanstalk Deployment Guide

## Prerequisites
- AWS Account with appropriate permissions
- AWS CLI installed and configured
- EB CLI (Elastic Beanstalk Command Line Interface)
- Git installed

## Installation

### 1. Install AWS CLI
```bash
# Windows
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Or via pip
pip install awscliv2
```

### 2. Install EB CLI
```bash
pip install awsebcli
```

### 3. Configure AWS Credentials
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-east-1 (or your preferred region)
# Default output format: json
```

## Deployment Steps

### 1. Initialize Elastic Beanstalk
```bash
eb init
# Select a region (or press enter for us-east-1)
# Select "Create a new application" if needed
# Application name: form-app
# Select Python platform
# Select Python 3.11
# Do you want to set up SSH? (y/n) - recommend 'y' for easier management
```

### 2. Create Environment
```bash
eb create form-app-env
# Wait for environment creation (5-10 minutes)
# This creates an EC2 instance and load balancer
```

### 3. Deploy Application
```bash
# Deploy latest code
eb deploy

# Or deploy with specific message
eb deploy --message "Deploying form validation app"
```

### 4. Monitor Deployment
```bash
# View environment status
eb status

# View logs
eb logs

# Open application in browser
eb open

# SSH into EC2 instance
eb ssh
```

## Additional Commands

```bash
# List all environments
eb list

# Switch to different environment
eb use <environment-name>

# Scale environment (add more instances)
eb scale 2

# Terminate environment
eb terminate

# View recent events
eb events -f

# Set environment variables
eb setenv SECRET_KEY=your-secret-key

# Configure domain
eb create form-app-prod --cname form-app.elasticbeanstalk.com
```

## Important Configuration Notes

### Edit Environment Configuration
Edit `.elasticbeanstalk/config.yml`:
- `application_name`: Your app name
- `environment`: Your environment name
- `default_region`: AWS region
- `default_platform`: Python version

### Update Application Settings
Edit `.ebextensions/app.config`:
- `InstanceTypes`: Change t3.micro to t3.small/t3.medium for more resources
- `EnvironmentType`: Set to "SingleInstance" for non-production
- `LoadBalancerType`: Use "application" for web apps

### Update App-Specific Settings
Edit `.ebextensions/python.config`:
- `WSGIPath`: Already set to `form_app:app`
- `PYTHONPATH`: Configured for proper module imports

## Production Security Checklist

- [ ] Change SECRET_KEY in form_app.py or use environment variable
- [ ] Set DEBUG = False in production
- [ ] Configure HTTPS/SSL certificate via AWS Certificate Manager
- [ ] Update CSRF trusted hosts in Flask configuration
- [ ] Configure RDS database if needed
- [ ] Set up proper IAM roles and permissions
- [ ] Enable auto-scaling policies
- [ ] Configure CloudWatch alarms and monitoring
- [ ] Set up application logs to CloudWatch or S3
- [ ] Test email validation service

## Environment Variables

Set environment variables via EB:
```bash
eb setenv FLASK_ENV=production
eb setenv SECRET_KEY=your-secret-key-here
eb setenv MAIL_SERVER=smtp.example.com
eb setenv MAIL_PORT=587
```

Or add to `.ebextensions/app.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
    SECRET_KEY: your-secret-key
```

## Troubleshooting

### Application not loading
```bash
# Check logs
eb logs
eb ssh  # SSH into instance and check /var/log/eb-activity.log
```

### Port 5000 already in use
- EB uses gunicorn, not Flask development server
- This happens when deploying locally

### Database connection issues
- Ensure RDS security group allows EB instance access
- Check environment variables are set correctly

### Static files not loading
- Ensure templates/ folder exists at project root
- Update Flask config for static file serving if needed

## Cost Management

- **t3.micro**: ~$10/month (free-tier eligible)
- **t3.small**: ~$20/month
- **Load Balancer**: ~$16/month
- **Data transfer**: $0.02 per GB (after free tier)

To minimize costs:
- Use SingleInstance for development
- Use scheduled auto-scaling
- Consider AWS Lightsail as alternative for simple apps

## Next Steps

1. Configure production SECRET_KEY
2. Set up custom domain with Route 53
3. Enable SSL/TLS certificate
4. Configure auto-scaling
5. Set up CloudWatch monitoring
6. Configure email service (AWS SES)
7. Set up CI/CD pipeline with CodePipeline

---
**Created**: March 21, 2026
**Application**: Professional Form Validation Web App
