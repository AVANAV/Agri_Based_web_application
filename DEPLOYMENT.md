# AgriMarket Deployment Guide

This guide covers deploying AgriMarket to production environments.

## Pre-Deployment Checklist

- [ ] Update `SECRET_KEY` in production
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure MongoDB Atlas (cloud) for production
- [ ] Set up environment variables (.env file)
- [ ] Hash all passwords in code
- [ ] Enable CSRF protection
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy
- [ ] Test all features thoroughly
- [ ] Set up error tracking (Sentry)

## Local Deployment

### 1. Set Up Environment
```bash
# Clone/extract project
cd d:\hifebfejf

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Application
```bash
# Copy and configure environment variables
copy .env.example .env

# Edit .env with your settings
# Ensure FLASK_ENV=development
```

### 3. Set Up Database
```bash
# Install MongoDB locally
# Or use MongoDB Atlas for cloud

# Initialize database collections
python -c "from database.db import users, products, orders, insurance, crop_predictions; print('Database initialized')"
```

### 4. Run Application
```bash
python app.py
```

Access at: http://localhost:5000

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      MONGO_URI: mongodb://mongo:27017/
    depends_on:
      - mongo
    volumes:
      - ./logs:/app/logs

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

### 3. Deploy with Docker

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f web

# Stop services
docker-compose down
```

## Heroku Deployment

### 1. Prepare Application

Update `app.py` for Heroku:
```python
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### 2. Create Procfile

```
web: gunicorn app:app
```

### 3. Create runtime.txt

```
python-3.9.18
```

### 4. Deploy to Heroku

```bash
# Install Heroku CLI
# heroku-cli.exe for Windows

# Login to Heroku
heroku login

# Create application
heroku create agrimarket-app

# Add MongoDB Atlas
heroku config:set MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/agri_app

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

## AWS Deployment

### 1. EC2 Setup

```bash
# Connect to EC2 instance
ssh -i key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update
sudo yum install python3 python3-pip
sudo yum install mongodb

# Clone repository
git clone <repo-url>
cd agrimarket

# Install requirements
pip3 install -r requirements.txt
pip3 install gunicorn
```

### 2. Start Application with Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### 3. Set Up Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 4. Set Up SSL with Let's Encrypt

```bash
sudo yum install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

## Production Security

### 1. Update Configuration

Create `production_config.py`:
```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
DEBUG = False
TESTING = False
```

### 2. Hash Passwords

Update `database/db.py`:
```python
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(name, email, password, role):
    hashed_password = generate_password_hash(password)
    user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "created_at": datetime.now(),
        "is_active": True
    }
    return users.insert_one(user)
```

### 3. Enable HTTPS

```python
from flask_talisman import Talisman

Talisman(app, force_https=True)
```

### 4. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    # ... login logic
```

### 5. CORS Configuration

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})
```

## Monitoring & Logging

### 1. Set Up Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('AgriMarket startup')
```

### 2. Sentry Error Tracking

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

### 3. Health Check Endpoint

```python
@app.route('/health')
def health_check():
    try:
        # Check database connection
        db_connection = list(users.find().limit(1))
        return jsonify({'status': 'healthy', 'timestamp': datetime.now()})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
```

## Database Backup

### MongoDB Backup Strategy

```bash
# Daily backup
mongodump --uri "mongodb+srv://user:pass@cluster.mongodb.net/agri_app" --out /backups/agri_app

# Automated backup with cron
0 2 * * * mongodump --uri "mongodb+srv://..." --out /backups/agri_app_$(date +\%Y\%m\%d)
```

## Performance Optimization

### 1. Database Indexing

Already configured in `database/db.py` with:
```python
users.create_index("email", unique=True)
products.create_index("farmer_id")
orders.create_index("buyer_id")
```

### 2. Caching

```bash
pip install flask-caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/products')
@cache.cached(timeout=60)
def get_products():
    # Cached for 60 seconds
```

### 3. CDN Integration

Serve static files through CloudFront or similar CDN for faster delivery.

## Continuous Integration/Deployment

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "agrimarket-app"
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   - Check firewall settings
   - Verify MongoDB is running
   - Check network connectivity

2. **500 Internal Server Error**
   - Check application logs
   - Verify environment variables
   - Check database connection

3. **High Memory Usage**
   - Check for memory leaks
   - Implement caching
   - Use connection pooling

4. **Slow Performance**
   - Add database indexes
   - Implement caching
   - Optimize queries
   - Use CDN for static files

## Support

For deployment help, contact: support@agrimarket.com

---

**Last Updated**: February 2026
