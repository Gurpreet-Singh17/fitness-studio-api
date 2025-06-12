# 🏋️‍♂️ Fitness Studio Booking API

This is a backend API built using **FastAPI** and **SQLAlchemy** that allows users to:
- Create and view fitness classes
- Book a class
- Retrieve bookings by email

---

## ⚙️ Setup Instructions


```bash

1. Clone the Repository
git clone https://github.com/Gurpreet-Singh17/fitness-studio-api
cd fitness-studio-api

Switch to the correct branch:
git checkout master


2. Create a Virtual Environment and Activate It
python -m venv venv
# For Linux/Mac
source venv/bin/activate
# For Windows
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

🚀 Running the App Locally
uvicorn BookClasses.main:app --reload

Visit the API at:
📍 http://127.0.0.1:8000

Interactive Swagger UI:
📘 http://127.0.0.1:8000/docs

🌱 (Optional) Add Seed Data
After the server runs once and the database is created, you can populate it with sample classes:
python seed.py


📮 Sample API Requests

✅ Health Check
curl -X GET http://127.0.0.1:8000/healthy


📘 Create a Class
curl -X POST http://127.0.0.1:8000/classes/ \
-H "Content-Type: application/json" \
-d '{
  "name": "Zumba",
  "dateTime": "2025-07-01T08:00:00",
  "instructor": "Aarav",
  "availableSlots": 20
}'


📋 Get All Classes
curl -X GET http://127.0.0.1:8000/classesall


⏳ Get Upcoming Classes
curl -X GET http://127.0.0.1:8000/classes


🧾 Book a Class
curl -X POST http://127.0.0.1:8000/book \
-H "Content-Type: application/json" \
-d '{
  "class_id": 1,
  "client_name": "Gurpreet",
  "client_email": "gur@gmail.com"
}'


📧 Get Bookings by Email
curl -X GET "http://127.0.0.1:8000/bookings?email=gur@gmail.com"


🧪 Running Tests
pytest
Make sure you're using the correct virtual environment and that pytest is installed.


📂 Project Structure
fitness-studio-api/
├── BookClasses/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
├── Test/
│   ├── test_main.py
│   ├── utils.py
├── seed.py
├── requirements.txt
├── README.md
├── LICENSE


🧑‍💻 Author
Gurpreet Singh
LinkedIn • GitHub