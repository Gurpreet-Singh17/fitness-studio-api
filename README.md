# 🏋️‍♂️ Fitness Studio Booking API

This is a backend API built using **FastAPI** and **SQLAlchemy** that allows users to:
- Create and view fitness classes
- Book a class
- Retrieve bookings by email

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Gurpreet-Singh17/fitness-studio-api
cd fitness-studio-api


2. Create a Virtual Environment and Activate It
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows


3. Install Dependencies
pip install -r requirements.txt

4. (Optional) Add Seed Data
bash
Copy
Edit
python seed.py
This will populate the database with sample classes.

🚀 Running the App Locally
bash
Copy
Edit
uvicorn BookClasses.main:app --reload
Visit the API at:
📍 http://127.0.0.1:8000

Interactive Swagger UI is available at:
📘 http://127.0.0.1:8000/docs

📮 Sample API Requests
✅ Health Check
bash
Copy
Edit
curl -X GET http://127.0.0.1:8000/healthy
📘 Create a Class
bash
Copy
Edit
curl -X POST http://127.0.0.1:8000/classes/ \
-H "Content-Type: application/json" \
-d '{
  "name": "Zumba",
  "dateTime": "2025-07-01T08:00:00",
  "instructor": "Aarav",
  "availableSlots": 20
}'
📋 Get All Classes
bash
Copy
Edit
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
Python Backend Assignment/
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

🧑‍💻 Author
Gurpreet Singh
LinkedIn | GitHub

