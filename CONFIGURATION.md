# Configuration Guide

## Environment Setup

### Backend Configuration

#### 1. Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

#### 2. Backend Environment Variables (.env)

Located in `backend/.env`:

```env
# Flask Configuration
FLASK_ENV=development              # development or production
FLASK_DEBUG=True                   # Enable debug mode
FLASK_APP=app:create_app           # Application entry point
FLASK_PORT=5000                    # Server port

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5000

# Security
SECRET_KEY=your-secret-key-here    # Change in production!

# Optional: API Rate Limiting
# API_RATE_LIMIT=100/hour
# API_TIMEOUT=30
```

#### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Installed Packages:**
- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - Cross-origin requests
- requests 2.31.0 - HTTP client
- beautifulsoup4 4.12.2 - HTML parsing
- lxml 4.9.3 - XML/HTML processing
- python-dotenv 1.0.0 - Environment management
- Pillow 10.1.0 - Image processing
- validators 0.22.0 - Data validation
- dnspython 2.4.2 - DNS operations

### Frontend Configuration

#### 1. Frontend Environment Variables (.env)

Located in `frontend/.env`:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:5000/api

# Optional: Analytics
# REACT_APP_ANALYTICS_ID=your-id

# Optional: Environment
# REACT_APP_ENV=development
```

#### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

**Key Packages:**
- react 18.2.0 - UI framework
- react-dom 18.2.0 - React rendering
- axios 1.6.0 - HTTP client
- chart.js 4.4.0 - Chart library
- react-chartjs-2 5.2.0 - React charts
- react-scripts 5.0.1 - Build tools

---

## Running the Application

### Development Mode

**Terminal 1 - Start Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm install
npm start
```

### Production Mode

**Backend:**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-key
python run.py
```

**Frontend:**
```bash
npm run build
# Serve build folder with a static server
```

---

## Port Configuration

| Service | Default Port | Environment Variable | Usage |
|---------|--------------|----------------------|-------|
| Backend API | 5000 | FLASK_PORT | Flask server |
| Frontend Dev | 3000 | (npm default) | React dev server |
| Frontend Build | 3000 | (custom server) | Production serve |

### Change Ports

**Backend:**
```bash
# Set in .env or command line
export FLASK_PORT=8000
python run.py
```

**Frontend:**
```bash
# Modify package.json or use PORT env var
PORT=3001 npm start
```

---

## API Configuration

### CORS Setup

**For Local Development:**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5000,http://localhost:3001
```

**For Production:**
```env
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

### API Endpoints

All endpoints are prefixed with `/api/`:
- Base URL: `http://localhost:5000/api`
- Production: `https://yourdomain.com/api`

---

## Database Configuration (Optional)

For future database integration:

```env
# Database
DB_TYPE=postgresql              # postgresql, mysql, sqlite
DB_HOST=localhost
DB_PORT=5432
DB_NAME=website_analyzer
DB_USER=your_username
DB_PASSWORD=your_password
```

---

## Logging Configuration

**Backend Logging:**

Create `backend/logging.conf`:
```ini
[loggers]
keys=root

[handlers]
keys=console,file

[formatters]
keys=standard

[logger_root]
level=INFO
handlers=console,file

[handler_console]
class=StreamHandler
level=DEBUG
formatter=standard
args=(sys.stdout,)

[handler_file]
class=FileHandler
level=DEBUG
formatter=standard
args=('app.log',)

[formatter_standard]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

---

## Performance Tuning

### Backend Optimization

```python
# In app/__init__.py
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Caching
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
```

### Frontend Optimization

**Update frontend/.env:**
```env
# Build optimization
GENERATE_SOURCEMAP=false
```

**Update webpack (in package.json):**
```json
{
  "scripts": {
    "build": "cross-env NODE_ENV=production react-scripts build"
  }
}
```

---

## Security Configuration

### Backend Security

```env
# Security Headers
SECURE_HEADERS=True

# Session Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# API Keys (if implemented)
API_KEY_VALIDATION=True
```

### Frontend Security

```env
# Content Security Policy
REACT_APP_CSP_ENABLED=true
```

---

## Deployment Configuration

### Environment Variables for Production

**Backend:**
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-secure-random-key-here
CORS_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
LOG_LEVEL=WARNING
```

**Frontend:**
```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENV=production
GENERATE_SOURCEMAP=false
```

### Server Configuration

**Using Gunicorn (recommended for Flask):**

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

**Using PM2 (for Node if needed):**
```bash
npm install -g pm2
pm2 start npm -- start
pm2 save
```

---

## Troubleshooting Configuration

### Issue: CORS Errors

**Solution:**
```env
# Ensure CORS_ORIGINS matches frontend URL
CORS_ORIGINS=http://localhost:3000

# Or for production
CORS_ORIGINS=https://yourdomain.com
```

### Issue: API Connection Failed

**Solution:**
```env
# Check API_URL in frontend .env
REACT_APP_API_URL=http://localhost:5000/api

# Verify backend is running
# Test: curl http://localhost:5000/api/health
```

### Issue: Port Already in Use

**Solution:**
```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process or change port
export FLASK_PORT=8000
```

### Issue: Module Not Found

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# or npm
rm -rf node_modules package-lock.json
npm install
```

---

## Configuration Checklist

- [ ] Python virtual environment created and activated
- [ ] Backend requirements installed
- [ ] Backend .env configured
- [ ] Frontend dependencies installed
- [ ] Frontend .env configured
- [ ] Ports are available (5000, 3000)
- [ ] CORS origins configured
- [ ] Security keys set (change from defaults)
- [ ] Database configured (if using)
- [ ] Logging configured
- [ ] API connectivity tested

---

## Reference

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [npm Documentation](https://docs.npmjs.com/)

---

For more information, see [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)
