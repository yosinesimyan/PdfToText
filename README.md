![image](https://github.com/user-attachments/assets/50f362b1-3f4c-41ee-ae73-ac537bcd6ae7)


# PdfToText
this project introduce a pdf to text convertion using python

# About the project

This project is a simple REST API built with Flask that enables users to upload pdf files, keep them in s3 bucket and convert them to text. the data will be kept in MySql Databaes and will be available to the user anytime.

# CI/CD

the project demonstrate a Ci/Cd pipeline using Jenkins

## Getting Started

To get started with this project, follow the instructions below.

### Prerequisites

- Python 3.x
- MySql Database(on premise or on docker in aws ec2 instance)
- Aws account
- Jenkins server
- Dockerhub account

### Installation

1. Clone the repository:

git clone https://github.com/yosinesimyan/PdfToText.git

2. in aws consule add user jenkins.
3. attach the user ec2fullaccess role
4. add role to the user named AttachRole with custom inline:
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "iam:PassRole"
            ],
            "Resource": "*"
        }
    ]
5. configure jenkins pipline to use github scm
6. build the jankins pipeline

The application should now be running on http://aws.public.ip:5000/.

### Usage

create an account usimg SignIn method
Login to your account
upload your PDF file
get the list of your PDF files with the text extracted from them

