# Loan Approval Prediction System — PythonAnywhere Deployment Guide

## Project Structure
```
loan_app/
├── app.py                  ← Flask application
├── wsgi.py                 ← WSGI entry point for PythonAnywhere
├── requirements.txt        ← Python dependencies
├── sample_loan_data.csv    ← Your dataset (upload this!)
├── trained_model.pkl       ← Auto-generated on first run
└── templates/
    └── index.html          ← Frontend UI
```

---

## Step-by-Step Deployment on PythonAnywhere

### 1. Create a PythonAnywhere Account
- Go to https://www.pythonanywhere.com and sign up (free tier works).

### 2. Upload Your Files
- In the PythonAnywhere dashboard → **Files** tab
- Create a folder: `loan_app/` (inside your home directory)
- Upload all files:
  - `app.py`
  - `wsgi.py`
  - `requirements.txt`
  - `sample_loan_data.csv`  ← **Required for model training**
  - `templates/index.html`

### 3. Open a Bash Console
- Dashboard → **Consoles** → **Bash**

### 4. Install Dependencies
```bash
cd ~/loan_app
pip install -r requirements.txt --user
```

### 5. Configure the Web App
- Dashboard → **Web** tab → **Add a new web app**
- Choose: **Manual configuration** → **Python 3.10**
- In the **WSGI configuration file** section, click the link to edit it
- Replace **all** contents with what's in `wsgi.py`
- **Change `YOUR_USERNAME`** to your actual PythonAnywhere username

### 6. Set Source Code & Working Directory
- **Source code**: `/home/YOUR_USERNAME/loan_app`
- **Working directory**: `/home/YOUR_USERNAME/loan_app`

### 7. Reload the Web App
- Click the big green **Reload** button on the Web tab

### 8. Visit Your Site
- Your app will be live at: `https://YOUR_USERNAME.pythonanywhere.com`

---

## How the App Works
1. On first load, Flask reads `sample_loan_data.csv`, trains the Logistic Regression model, and saves it as `trained_model.pkl`.
2. The user fills in the form on the web page.
3. The form sends a POST request to `/predict`.
4. Flask encodes the inputs, runs the model, and returns approval status + probability.

---

## Troubleshooting
| Issue | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt --user` in Bash console |
| `FileNotFoundError: sample_loan_data.csv` | Make sure the CSV is uploaded to `loan_app/` |
| 500 Server Error | Check the **Error log** on the Web tab |
| Model not found | Delete `trained_model.pkl` and reload — it will retrain automatically |
