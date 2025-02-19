# 🚗 Service Track Web

## 📌 Features  
✅ User authentication (admin & regular users)  
✅ Manage cars and their service history  
✅ Export service records  
✅ MySQL database support  

## 🏗 Prerequisites  
- **Python 3.10+**  
- **MySQL** (running on Windows/macOS)  

## 📥 Clone the Repository  
```sh
git clone https://github.com/tonantr/service-track-web.git
cd service-track-web

## Generate the requirements.txt
pip freeze > requirements.txt

###  Install Dependencies
pip install -r requirements.txt

## 🚀 Running the Application
macOS:
python3 main.py
Windows:
python main.py

## 🚀 Running the Application on a Server
macOS:
python3 -m waitress --host=0.0.0.0 --port=8000 main:app
windows:
python -m waitress --host=0.0.0.0 --port=8000 main:app