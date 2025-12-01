![Extension Logo Screenshot](/static/images/Logo.png)

# Insecure and Secure Blog Application

## By Nyk077771

A Simple Blog Creating Application that is built with Secure and Insecure versions.

## About:

This is an application that was built with two branch versions (Insecure and Secure). Built as part of the Secure Application Programming module for my BSHCCYBE4 program. Its purpose is to demonstrate the XSS, and SQL injection, along with secure and insecure development practices.

The application itself is a simple web blog where users can:

- Register and Login with their details.
- Create, view and delete blog posts.
- Search for blog content.

## :bangbang: Important to Note :bangbang:

The application contains two versions: Secure and Insecure.

- **Secure** Contains vulnerabilities by default for educational purposes.
- **Insecure** Fixes the Vulnerabilities encountered in the Insecure versions and adds extra security features.

**Please DO NOT employ the insecure verion**

## Learning Objectives

This project addresses the following learning requirements:

**LO2** - Evaluate, develop and implement programming solutions for secure development.
**LO3** - Appraise trade-ofs in performance, usability, and other quality attributes.
**LO4** - Identify, analyze and evaluate the ethical effects and impacts of design decisions.

## Features

### Blog Features:

- User Registration.
- User AUthentication.
- Session Control.
- Blog Search.
- Blog Creation.
- Role-based acces.
- Responsive UI.

### Insecure Version Features:

- SQL Injection Vulnerability.
- Cross-Site Scripting (XSS) - Reflected, DOM, and Stored types.
- Sensitive Data Exposure.
- Hardcoded Secrets.
- Highly Detailed Error Messages.
- Missing Input Validation.
- Missing Security Headers.

### Secure Version Features:

- SQL Injection Prevention - Parameterised SQL queries.
- XSS Prevention - Input Validation and output ancoding.
- Password hashing with bcrypt.
- CSRF tokens (CSRF Attack Prevention).
- Security headers (X-XSS-Protection, Content-type, Strict-Transport-Security, Content-Security-Policy).
- System logging.
- Generic error messages given.

## Technology

- **Frontend Web Page**: HTML5, CSS, Bootstrap, JavaScript
- **Backend Server**: Python, Flask
- **Database**: MySQL
- **Security** bcrypt, flask-talisman, flask-wtf
- **Testing** Selenium, OWASP ZAP, Lighthouse

## Installation

### System Requirements:

- Python 3.14
- MySQL 8.0
- Python's pip
- Git

### 1. Clone Repository

```bash
git clone https://github.com/Nyko77771/insecure_blog.git
cd insecure_blog
```

### 2. Choose Branch

**_Insecure_**:

```bash
git checkout insecure
```

**_Secure_**

```bash
git checkout secure
```

### 3. Create Virtual Environment

Windows:

```bash
python -m venv virt
virt\Scripts\activate
```

MAC/Linux:

```bash
python3 -m venv virt
```

### 4. Activate Virtual Environment

Windows:

```bash
virt\Scripts\activate
```

MAC/Linux:

```bash
source virt/bin/activate
```

### 5. Install Dependancies

```bash
pip install -r requirements.txt
```

### 6. Configure Database

- Create '.env' file in root folder.
- Add to the file your MySQL details (Replace '...' with your details):

```env
# Database Configuration:
MYSQL_HOST=...
MYSQL_USER=...
MYSQL_PASSWORD=...
MYSQL_DB_NAME=...

# Flask Configuration:
FLASK_SECRET_KEY=...
FLASK_ENV=development
```

**Note**: Insecure version has hard coded security credentials on purpose.

### 7. Initialise Database

```bash
mysql -u ... -p < database/setup.sql
```

### 8. Run app.py

```bash
python app.py
```

Access the application at: https://localhost:5000

## Database Default Accounts

Insert below default user into your MySQL database/

| _Username_ | _Password_ | _Role_ |
| nykyta | nyk123 | admin |
| testuser | pass123 | regular |

MySQL Code:

```sql
INSERT INTO users (username, email, password, role) VALUES ('nykyta', 'nyk@email.com', 'nyk123', 'admin');
INSERT INTO users (username, email, password, role) VALUES ('testuser', 'test@email.com', 'pass123', 'regular');
```

- **NOT To be used in Production**

## Tests

_Use the default Accounts above or create your own._

### Manual Testing (Insecure Version)

#### SQL Injection

**Login Page**

```
Username: admin' OR '1'='1' --
Password: password
```

#### XSS (Reflected)

**Home Page (Search Function)**

```
Search: <script>alert(`Reflected XSS`)</script>
```

#### XSS (Stored)

**Creation + Blog Page (Blog Title Storage)**

```
Title: <script>alert(`Stored XSS`)</script>
```

#### XSS (DOM)

**Blog Page (URL Injection)**

```
Browser URL: https://localhost:5000/blog?welcome=<script>alert(`DOM XSS`)</script>
```

### Automated Testing

#### OWASP ZAP

1. Install OWASP ZAP (https://www.zaproxy.org/download/)

2.Run Scan

```
Target: https://localhost:5000
Attack Mode: Standard
```

3. Analyse the alerts. Check for XSS and SQL Injection Vulnerabilities.

#### Selenium

```bash
python tests/test.py
```

Tests:

- User registration.
- Login functionality.
- Blog creation.
- Search.

## Contributions

This is an educational open source development project. All types of contributions are welcome.

## Contact

**Developer**: Nykyta McDonald
:email: x22140115@student.ncirl.ie
:link: @Nyko77771

For any issues or question or questions, either email or open an issue on GitHub.

## License

This porject is licensed unfder the MIT license.

**For Educational Use Only**: This application is strictly made for educational purpose only. Insecure version should not be used for production purpose.
