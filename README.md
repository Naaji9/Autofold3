# Updated AutoFold (ready to use )


---

### **1. Python Script Files**
- **`automate_prediction.py`**: The main Python script that automates the AlphaFold process.
  

---

### **2. Input and Output Example Files**
- **Example Input File**:
  - Include a sample Excel file (e.g., `example_input.xlsx`) with properly formatted columns (`variant`, `fasta_sequence`).
- **Output Directory Structure**:
  - `ProteinPrediction/Output` folder in the repository to show where outputs will be saved.

---

### **3. `requirements.txt`**
- A file listing all the Python dependencies required for the project.  
  Example content:
  ```
  selenium
  pandas
  gemmi
  webdriver-manager
  ```

`README.md`

```markdown
# Protein Prediction Automation

This project is a web-based application that automates the process of protein structure prediction using AlphaFold 3.
It allows users to upload their protein datasets, enter their credentials, and track the automation process step-by-step through a streamlined frontend interface.

## Features

- Automated Protein Prediction: Uses AlphaFold 3 to predict protein structures from input sequences.
- Real-Time Status Updates: Users can see step-by-step feedback on the automation process.
- Simple Frontend Interface: A user-friendly React interface for easy data submission and status tracking.
- Secure Data Handling: Credentials are securely managed without persistent storage.

## Technologies Used

- Frontend: React, HTML, CSS
- Backend: Django, Django REST framework
- Automation: Selenium, Python
- Other Libraries: Pandas for data processing, Gemmi for CIF to PDB conversion

## Project Structure

```plaintext
ProteinPrediction/
├── ProteinPrediction/
│   ├── settings.py
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py
├── automation/
│   ├── views.py             # Django view handling data submission
│   ├── urls.py              # URL routing for automation app
│   ├── automation_script.py # Python script for Selenium automation
│   └── templates/
│       └── automation/
└── frontend/
    ├── src/
    │   ├── App.js           # Main React component
    │   ├── components/
    │   │   └── ProteinPredictionForm.js
    │   └── assets/
    │       └── logo.png     # Project logo
    └── public/
```

## Installation

### Backend Setup (Django)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/combilab-furg/AutoFold.git
   cd protein-prediction-automation
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django djangorestframework selenium pandas gemmi openpyxl webdriver_manager
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the Django server**:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup (React)

1. **Navigate to the frontend folder**:
   ```bash
   cd Downloads/AutoFold-main/protein-prediction-frontend
   ```
2. # Install Node.js
Ensure you have a supported version of Node.js. You can use nvm (Node Version Manager) to install and manage Node.js.

Install Node.js Using nvm
bash
Copy code
# Install nvm if not already installed
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
source ~/.bashrc
```

# Install Node.js
```
nvm install 18
```

# Use the installed Node.js version
```
nvm use 18
```

# Verify the Node.js version
```
node -v
```

3. **Install dependencies**:
   ```bash
   npm install
   ```

4. **Start the React development server**:
   ```bash
   npm start
   ```


## Troubleshooting
1. Outdated Node.js Version
If you see warnings or errors about unsupported engine versions during npm install, ensure that your Node.js version is >= 16.x. Use nvm to upgrade Node.js.

2. Dependency Vulnerabilities
After installation, you may see vulnerabilities in dependencies. Fix them with:

```bash
Copy code
npm audit fix
npm audit fix --force
```
3. Clearing Dependencies
If you encounter any issues, clear the node_modules directory and reinstall dependencies:

```bash
Copy code
rm -rf node_modules package-lock.json
npm install
Recommended Software Versions
Node.js: v18.x (Tested and working)
npm: v8.x
```

**Start the React development server**:
   ```bash
   npm start


## Usage

1. Open the React app in your browser at `http://localhost:3000`.
2. Enter your email, password, and upload the `proteins.xlsx` file.
3. Click **Submit** to start the automation process.
4. Track the progress through real-time status updates on the frontend.

## Project Notes

- Ensure `chromedriver` is correctly installed as it’s used by Selenium for automation.
- The project is configured for local development. Make sure the backend and frontend are running on compatible local ports.

## License

This project is licensed under the MIT License.
```



