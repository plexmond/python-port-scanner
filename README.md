# Port Scanner

This is a Python port scanning web application built with Flask. It allows you to scan a specified range of ports or specific common ports for a hostname / IP-address. The application also supports multithreaded scanning and getting HTTP headers. Scanning results can be emailed to the user using the MailGun API.

## Portscanner Features

- Custom port range scanning
- Common ports scanning
- Single port scanning
- Concurrent port scanning for improved speed
- HTTP header scanning
- Send scanning results to email

## Disclaimer
Port scanning is a technique used to identify open ports on a target system. While this application provides a handy way to perform port scanning, it is essential to note the following:

- Permission: Before conducting any port scanning activities, ensure that you have the necessary authorization from the target system owner or network administrator. Unauthorized port scanning is illegal and may result in legal consequences.

- Ethical Use: Port scanning should only be performed on systems or networks that you have explicit permission to test. It is crucial to respect the privacy and security of others and adhere to ethical guidelines when using this application.

- Network Impact: Port scanning can generate network traffic and potentially impact the performance of the target system or network. It is recommended to conduct port scanning activities responsibly and considerate of the potential impact on network resources.

- Accuracy and Reliability: While this application aims to provide accurate and reliable port scanning results, there can be false positives or false negatives. It is advisable to validate the results obtained from this application using other security assessment techniques.

By using this application, you acknowledge that you understand and agree to these considerations regarding port scanning.



## Installation and running the app

To install and run this project, you need to follow these steps:

### 1. Clone the Repository

You can clone the repository to your local machine by running the following commands:

```bash
git clone https://git.fhict.nl/I508065/pyscan-webapp.git
```


### 2. Requirements

You need to install Python 3.11 and pip on your machine. After that, you can install the project dependencies with:

```bash
pip install -r requirements.txt
```

### 3. Configuration

Before running the application, you will need to setup several settings:

- Mailgun domain name
- Mailgun API key
- Sender's email

These settings are located in `config.py`. You need to make this file yourself in the project root directory.
You can edit this file with the necessary values:

```python
class Config:
    MAILGUN_DOMAIN_NAME = 'your-mailgun-domain'
    MAILGUN_API_KEY = 'your-mailgun-api-key'
    FROM_EMAIL = 'your-email'
```

### 4. Running the Application

You can run the application locally with:

```bash
python main.py
```

The application will be available at `http://localhost:5000`.

### 5. Running in Docker

You can also run the application as a Docker container. First, build the Docker image:

```bash
docker build -t port-scanner .
```

Then, run the Docker container:

```bash
docker run -p 5000:5000 port-scanner
```

The application will be available at `http://localhost:5000`.

## Usage

Navigate to `http://localhost:5000` in your web browser. Enter the hostname and choose the scan options. After submitting the input form, you will be presented with the scan results. You can also choose to receive the results by email by filling it in.


## Contact

Created by [@I508065](https://git.fhict.nl/I508065)