# PdfToTExt
this project introduce a pdf to text convertion using python

# About the project

This project is a simple REST API built with Flask that enables users to upload pdf files, keep them in s3 bucket and convert them to text. the data will be kept in MySql Satabaes and will be available to the user anytime.

# CI/CD

the project demonstrate a Ci/Cd pipeline using Jenkins

## Getting Started

To get started with this project, follow the instructions below.

### Prerequisites

- Python 3.x
- Flask
- Aws account
- Jenkins
- Dockerhub account

### Installation

1. Clone the repository:

git clone https://github.com/yosinesimyan/PdfToText.git

2. Navigate to the project directory:

cd app

3. Install the dependencies:

pip install -r requirements.txt

4. Run the Flask application:

python app.py

The application should now be running on http://127.0.0.1:5000/.

### Usage

create an account usimg SignIn method
Login to your account
upload your PDF file
get the list of your PDF files with the text extracted from them

