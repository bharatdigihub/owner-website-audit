# Installation & Deployment Guide

## Complete Installation Instructions

### System Requirements

**Minimum:**
- Python 3.8 or higher
- Node.js 14 or higher
- 2GB RAM
- 500MB disk space

**Recommended:**
- Python 3.10+
- Node.js 18+
- 4GB RAM
- 1GB disk space

---

## Step-by-Step Installation

### Phase 1: Prepare Environment

#### 1.1 Clone or Extract Project
```bash
# If using git
git clone <repository-url>
cd website-checker

# Or if already extracted
cd website-checker
```

#### 1.2 Verify Directory Structure
```bash
# You should see these directories
ls -la
# Output should include:
# backend/
# frontend/
# .github/
# And several .md files
```

---

### Phase 2: Backend Installation

#### 2.1 Navigate to Backend
```bash
cd backend
```

#### 2.2 Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Verify Virtual Environment is Active
```bash
# You should see (venv) in your prompt
# On Windows, try:
where python
# Should show path with venv\Scripts

# On macOS/Linux:
which python
# Should show path with venv/bin
```

#### 2.4 Upgrade pip
```bash
pip install --upgrade pip
```

#### 2.5 Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed Flask-3.0.0 Flask-CORS-4.0.0 ...
```

#### 2.6 Verify Installation
```bash
# Test Flask installation
python -c "import flask; print(f'Flask {flask.__version__} installed')"

# Test BeautifulSoup
python -c "import bs4; print(f'BeautifulSoup {bs4.__version__} installed')"
```

#### 2.7 Configure Backend
```bash
# View the .env file
cat .env

# Verify these settings are present:
# FLASK_ENV=development
# FLASK_DEBUG=True
# FLASK_APP=app:create_app
# FLASK_PORT=5000
```

---

### Phase 3: Frontend Installation

#### 3.1 Navigate to Frontend
```bash
# From project root, if you were in backend/
cd ../frontend

# Or if in new terminal
cd frontend
```

#### 3.2 Check Node.js Installation
```bash
node --version    # Should be v14+
npm --version     # Should be v6+
```

#### 3.3 Install Node Dependencies
```bash
npm install
```

**Expected Output:**
```
added XXX packages in XXs
```

#### 3.4 Verify Installation
```bash
npm list react react-dom axios
```

#### 3.5 Configure Frontend
```bash
# Check .env file
cat .env

# Should contain:
# REACT_APP_API_URL=http://localhost:5000/api
```

---

## Phase 4: Verify Installation

### 4.1 Backend Verification

```bash
# In backend directory with venv activated
python -c "
from app import create_app
app = create_app()
print('✓ Flask app created successfully')
print(f'✓ Flask routes registered: {len(app.url_map._rules)}')
"
```

### 4.2 Frontend Verification

```bash
# In frontend directory
npm ls react react-dom
# Should show installed versions
```

### 4.3 File Structure Verification

```bash
# From project root
# Verify backend files
ls backend/app/analyzers/
# Should show:
# base.py
# performance.py
# security.py
# seo.py
# code_standards.py
# user_friendliness.py
# user_behavior.py

# Verify frontend files
ls frontend/src/components/
# Should show tab components and common components
```

---

## Phase 5: Run the Application

### Starting for the First Time

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py
```

**Expected Output:**
```
WARNING in app.run() because this is a development server.
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view website-analyzer in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

### 5.1 Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

### 5.2 Test the Application

1. **Enter a test URL:**
   - `https://example.com`
   - `https://github.com`
   - `https://wikipedia.org`

2. **Click "Analyze Website"**

3. **Wait for analysis to complete** (30-60 seconds)

4. **View the results**
   - Overview tab shows all scores
   - Click individual tabs for detailed analysis
   - Review recommendations

---

## Phase 6: Build for Production

### 6.1 Build Frontend

```bash
cd frontend
npm run build
```

**Output:**
```
The build folder is ready to be deployed.
You may serve it with a static server.
```

### 6.2 Build Backend (Optional)

For production, use a WSGI server:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

### 6.3 Deployment Checklist

- [ ] Update `FLASK_ENV=production`
- [ ] Set a strong `SECRET_KEY`
- [ ] Update `CORS_ORIGINS` with your domain
- [ ] Update `REACT_APP_API_URL` with your API domain
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use HTTPS in production
- [ ] Set up proper database (if needed)
- [ ] Configure logging
- [ ] Enable security headers
- [ ] Set up monitoring/alerts

---

## Troubleshooting Installation

### Issue 1: Python Version Too Old
```bash
# Check Python version
python --version

# Solution: Install Python 3.8+
# Download from python.org or use:
# macOS: brew install python@3.10
# Ubuntu: sudo apt-get install python3.10
```

### Issue 2: Virtual Environment Not Activating
```bash
# Windows - Try full path:
"C:\full\path\to\venv\Scripts\activate.bat"

# macOS/Linux - Try:
bash venv/bin/activate
```

### Issue 3: pip Install Fails
```bash
# Upgrade pip first
pip install --upgrade pip

# Try again
pip install -r requirements.txt

# If still fails, try with --no-cache-dir
pip install --no-cache-dir -r requirements.txt
```

### Issue 4: npm Install Fails
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Issue 5: Port Already in Use
```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :5000

# Kill the process or use different port
export FLASK_PORT=8000
```

### Issue 6: CORS Errors
```bash
# In backend/.env, ensure:
CORS_ORIGINS=http://localhost:3000

# Restart backend server
```

### Issue 7: Connection Refused
```bash
# Verify both servers are running
# Backend: http://localhost:5000/api/health
# Should return: {"status":"healthy","message":"..."}

# If fails, restart backend with:
python run.py
```

---

## Verification Checklist

After Installation:

- [ ] Backend virtual environment created and activated
- [ ] Backend dependencies installed (`pip list` shows 9 packages)
- [ ] Backend server starts without errors
- [ ] Frontend dependencies installed (`npm list` shows packages)
- [ ] Frontend development server starts
- [ ] Frontend accessible at `http://localhost:3000`
- [ ] Backend API accessible at `http://localhost:5000/api/health`
- [ ] Analysis completes successfully
- [ ] Results display in dashboard
- [ ] All tabs work properly
- [ ] New analysis button works

---

## Common Commands

### Backend Commands
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run development server
python run.py

# Run with custom port
export FLASK_PORT=8000 && python run.py

# Deactivate virtual environment
deactivate
```

### Frontend Commands
```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Install new package
npm install package-name

# Update packages
npm update
```

---

## Performance Notes

- First analysis takes 30-60 seconds
- Subsequent analyses are faster (10-20 seconds)
- Large websites may take longer
- Network speed affects analysis time
- Consider implementing caching for frequently analyzed sites

---

## Next Steps After Installation

1. **Explore the Dashboard**
   - Analyze several websites
   - Review different analysis categories
   - Check recommendations

2. **Customize**
   - Update colors in CSS files
   - Add custom analyzers
   - Modify scoring logic

3. **Integrate**
   - Connect to database
   - Add user authentication
   - Implement history tracking

4. **Deploy**
   - Set up production server
   - Configure domain
   - Enable HTTPS
   - Monitor performance

---

## Support & Resources

### Documentation Files
- `README.md` - Complete project documentation
- `QUICKSTART.md` - Quick setup guide
- `CONFIGURATION.md` - Configuration details
- `ARCHITECTURE.md` - System architecture
- `PROJECT_SUMMARY.md` - Features overview

### External Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [npm Documentation](https://docs.npmjs.com/)

---

**Congratulations! Your Website Analyzer is now installed and ready to use! 🎉**
