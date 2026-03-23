@echo off
REM AWS Elastic Beanstalk Deployment Script for Windows

echo ================================
echo Form App - EB Deployment Script
echo ================================
echo.

REM Check if EB CLI is installed
eb --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: EB CLI is not installed!
    echo Please install it first:
    echo   pip install awsebcli
    pause
    exit /b 1
)

REM Check if AWS credentials are configured
aws sts get-caller-identity >nul 2>&1
if errorlevel 1 (
    echo ERROR: AWS credentials are not configured!
    echo Please run: aws configure
    pause
    exit /b 1
)

echo Step 1: Initializing Elastic Beanstalk...
call eb init -p "Python 3.11 running on 64bit Amazon Linux 2" --region us-east-1
if errorlevel 1 (
    echo ERROR: Failed to initialize EB
    pause
    exit /b 1
)

echo.
echo Step 2: Creating environment (form-app-env)...
echo This may take 5-10 minutes...
call eb create form-app-env
if errorlevel 1 (
    echo ERROR: Failed to create environment
    pause
    exit /b 1
)

echo.
echo Step 3: Deploying application...
call eb deploy
if errorlevel 1 (
    echo ERROR: Failed to deploy
    pause
    exit /b 1
)

echo.
echo ================================
echo ✓ Deployment Successful!
echo ================================
echo.
echo Opening application in browser...
call eb open

echo.
echo Useful commands:
echo   eb status         - Check environment status
echo   eb logs -f        - View live logs
echo   eb ssh            - SSH into EC2 instance
echo   eb events -f      - Watch events
echo   eb terminate      - Delete environment
echo.
pause
