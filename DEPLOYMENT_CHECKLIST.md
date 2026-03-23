# Quick Deployment Checklist

## Before Deploying to Elastic Beanstalk

### 1. Code Preparation
- [ ] Update `SECRET_KEY` in form_app.py or set as environment variable
- [ ] Set `DEBUG = False` for production
- [ ] Review all hardcoded configurations
- [ ] Ensure all imports are in requirements.txt
- [ ] Test application locally: `python form_app.py`

### 2. Project Structure Check
```
demo/
├── .ebextensions/          ✅ Created
│   ├── python.config       ✅ Fixed
│   └── app.config          ✅ Created
├── .elasticbeanstalk/      ✅ Created
│   └── config.yml          ✅ Created
├── .ebignore               ✅ Created
├── form_app.py             ✅ Ready
├── form_app_requirements.txt ✅ Updated (added gunicorn)
├── templates/
│   ├── index.html          ✅ Ready
│   └── about.html          (if exists)
└── README.md
```

### 3. Requirements Setup
- [ ] `pip install -r form_app_requirements.txt`
- [ ] Verify all packages install successfully
- [ ] Test application works locally

### 4. AWS Setup
- [ ] Create AWS account (or login to existing)
- [ ] Install AWS CLI
- [ ] Install EB CLI: `pip install awsebcli`
- [ ] Run `aws configure` with your AWS credentials
- [ ] Verify credentials work: `aws s3 ls`

### 5. Git Repository
- [ ] Initialize/update git: `git init` (if not done)
- [ ] Add files: `git add .`
- [ ] Commit: `git commit -m "Initial commit - EB ready"`
- [ ] All changes committed before EB deployment

### 6. Environment Configuration
- [ ] Edit `.elasticbeanstalk/config.yml`:
  - [ ] Set `application_name` to desired name
  - [ ] Set `default_region` (us-east-1, us-west-2, etc.)
  - [ ] Set `default_ec2_keyname` (optional, for SSH access)

### 7. Application Configuration
- [ ] Edit `.ebextensions/python.config`:
  - [ ] WSGI path is correct: `form_app:app`
  - [ ] Python path is set
  - [ ] CloudWatch logging enabled

- [ ] Edit `.ebextensions/app.config`:
  - [ ] Instance type set appropriately (t3.micro, t3.small, etc.)
  - [ ] Auto-scaling configured if needed
  - [ ] Load balancer type selected

### 8. Security Review
- [ ] Change SECRET_KEY before production
- [ ] CSRF protection enabled in Flask-WTF
- [ ] Email validation working
- [ ] Password requirements enforced
- [ ] Terms agreement checkbox required

### 9. Testing
- [ ] Form submission works locally
- [ ] All validation messages appear
- [ ] Password strength indicator works
- [ ] Error handling works
- [ ] No console errors in browser

---

## Deployment Commands (Quick Reference)

```bash
# Initialize EB (first time only)
eb init -p "Python 3.11 running on 64bit Amazon Linux 2" --region us-east-1

# Create environment
eb create form-app-env

# Deploy updates
eb deploy

# Monitor
eb open
eb logs -f
eb status
eb events -f

# SSH into server
eb ssh
```

---

## After Deployment

### Verify Deployment
- [ ] Open application: `eb open`
- [ ] Test form submission
- [ ] Check validation messages
- [ ] Verify no errors in logs: `eb logs`

### Configure Production
- [ ] Set environment variables: `eb setenv SECRET_KEY=xxxxx`
- [ ] Enable HTTPS/SSL certificate
- [ ] Configure custom domain
- [ ] Set up monitoring and alarms
- [ ] Configure auto-scaling policies

### Monitoring & Maintenance
- [ ] Check CloudWatch metrics
- [ ] Monitor application logs
- [ ] Set up email alerts
- [ ] Plan regular updates
- [ ] Monitor costs

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "import form_app failed" | Ensure WSGIPath is `form_app:app` |
| Port 5000 already in use | This is normal - EB uses gunicorn port |
| Form data not being processed | Check CSRF token in HTML form |
| Styling not loading | Verify static files path configuration |
| Large deployment time | Check instance logs: `eb logs` |

---

## Important Notes

⚠️ **Security**: 
- Never commit `.env` files with secrets
- Always use environment variables for sensitive data
- Enable HTTPS before going production

💰 **Cost Optimization**:
- t3.micro is free tier eligible
- Remove load balancer for development
- Use scheduled scaling for non-24/7 apps

---

**Status**: ✅ Ready for EB Deployment
**Last Updated**: March 21, 2026
