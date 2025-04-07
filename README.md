# AWS Resources Deletion Pipeline

A Jenkins-based/Github actions automated pipeline to detect and delete AWS resources across multiple accounts. Useful for cleaning up environments, saving costs, and maintaining cloud hygiene.

## 🚀 Features

- 🔁 **Cross-account resource deletion**
- 🤖 **Automated with Jenkins pipelines**
- 🐍 **Python-based deletion logic**
- 🛠️ **Customizable to fit your specific AWS cleanup needs**

---

## 🗂️ Project Structure

```bash
AWS-Resources-Deletion-Pipeline/
├── .github/workflows/         # GitHub Actions workflows 
├── deletion_script.py         # Main Python script for deletion logic
├── jenkins_pipeline.groovy    # Jenkins pipeline definition
├── requirements.txt           # Python dependencies
└── README.md                  # You're reading it!

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Malaroy123/AWS-Resources-Deletion-Pipeline.git
cd AWS-Resources-Deletion-Pipeline

### 2. Install Python dependencies

```
pip install -r requirements.txt

### 3. Configure AWS credentials
Make sure AWS CLI is installed and configured:
```
aws configure

Or set environment variables:
```
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

## 🧪 Usage
### 🔧 Manual Run (for testing)
```
python deletion_script.py

## 🌀 Jenkins Pipeline Run
- Import the jenkins_pipeline.groovy into your Jenkins job.
- Set up credentials and environment variables in Jenkins.
- Trigger the pipeline to start automated cleanup.

## 🧯 Caution
**This script deletes AWS resources. Double-check everything and ideally test in a non-production environment first!**
