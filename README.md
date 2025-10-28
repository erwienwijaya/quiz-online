# 🧠 Python Learning Quiz App

An **online quiz application** designed to support Python learning through interactive assessments. The app features **four quizzes** that evaluate learners understanding of fundamental Python concepts in an engaging and structured manner. The source code is built following the SOLID principles, ensuring a clean architecture, maintainable codebase, and high scalability for future enhancements.

---

## 🚀 Features

- Four Python-related quizzes  
- Simple and responsive UI built with **TailwindCSS**  
- Powered by **Flask** and **SQLite**  
- Uses **Font Awesome** for icons  
- Lightweight and easy to deploy locally

---

## 🛠️ Tech Stack

- **Python** 3.12  
- **Flask** 3.0  
- **SQLite**  
- **TailwindCSS**  
- **Font Awesome**

---

## ⚙️ Local Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/erwienwijaya/quiz-online.git
cd python-quiz-app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

macOS / Linux

```bash
source ./venv/bin/activate
```

Windows (PowerShell)

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application Locally

### 1. Set Environment Variables

macOS / Linux:

```bash
export FLASK_DEBUG=1
export FLASK_APP=run.py
export FLASK_ENV=development
```

Windows (PowerShell):

```bash
set FLASK_DEBUG=1
set FLASK_APP=run.py
set FLASK_ENV=development
```

### 2. Run Flask

```bash
flask run
```

### 3. Open in Browser

```bash
http://localhost:5000
```

### License

This project is open source and available under the MIT License.

### Author

Developed by Erwien Tjipta Wijaya