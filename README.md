# Face Recognition Attendance Management System (FRAS)

An automated, real-time biometric attendance management system built with Python, Django, MTCNN, and TensorFlow/Keras. FRAS eliminates manual roll-call processes by leveraging computer vision pipelines to detect faces from live video streams, extract facial feature embeddings, match identities against registered profiles, and log timestamped records automatically into a central web database.

---

## Key Features

- **Automated Detection & Alignment:** Uses Multi-task Cascaded Convolutional Networks (MTCNN) for precise face detection and alignment under varying lighting conditions.
- **Deep Learning Recognition:** Extracts high-dimensional facial embeddings using TensorFlow and Keras pre-trained models for identity verification.
- **Real-Time Stream Processing:** Processes live camera frames in real time with low latency to detect and label subjects.
- **Django Administrative Portal:** A web dashboard to register new users, manage profiles, monitor live recognition sessions, and analyze attendance history.
- **Automated Logging & Reporting:** Prevents duplicate logs per session and saves timestamped attendance entries directly to a database.

---

## System Architecture & Pipeline

```text
[ Video Input Feed ]
         │
         ▼
[ MTCNN Face Detection ]       ───► Detects Bounding Boxes & Facial Landmarks
         │
         ▼
[ Deep Feature Extraction ]    ───► Generates Embeddings (TensorFlow / Keras)
         │
         ▼
[ Vector Matching Engine ]     ───► Compares Vectors with Stored Profile Data
         │
         ▼
[ Django Backend & Database ]  ───► Records Timestamped Attendance Entries

```

## Tech Stack & Dependencies

* **Programming Language:** Python 3.8+
* **Web Framework:** Django
* **Computer Vision & Processing:** OpenCV, MTCNN
* **Deep Learning Libraries:** TensorFlow, Keras, NumPy
* **Database:** SQLite (Development) / PostgreSQL (Production)



## Project Structure
├── manage.py
├── requirements.txt
├── README.md
├── fras_core/              # Django core settings and URL configurations
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── attendance_app/         # Main app logic
│   ├── models.py           # Database models for user profiles and logs
│   ├── views.py            # Stream ingestion and administrative views
│   ├── utils.py            # Computer vision and model inference routines
│   ├── urls.py
│   └── templates/          # HTML templates for the web portal
└── dataset/                # Stored user profile vectors and images

## Complete Installation & Setup Guide
Follow these steps sequentially to set up and run the system locally on your machine:

### 1. Clone the Repository

- git clone [https://github.com/your-username/face-recognition-attendance.git](https://github.com/your-username/face-recognition-attendance.git)
- cd face-recognition-attendance

### 2. Set Up a Virtual Environment
#### On Linux / macOS:

- python3 -m venv venv
- source venv/bin/activate
- 
#### On Windows:

- python -m venv venv
- venv\Scripts\activate

### 3. Install Required Dependencies
#### Ensure you have pip updated, then run:

-pip install --upgrade pip
-pip install -r requirements.txt

### 4. Apply Database Migrations

#### Create the database tables for user profiles, attendance logs, and sessions:

- python manage.py makemigrations
- python manage.py migrate

### 5. Create an Administrative Superuser
##### Create an admin account to access the administrative web portal:
python manage.py createsuperuser

### 6. Run the Development Server
#### Start the Django server:
python manage.py runserver

#### Open your browser and go to http://127.0.0.1:8000/.

## How to Use the System
 1. Log In: Access the Django admin portal using your superuser credentials.

 2. Register Users: Create user profiles (e.g., students or employees) and collect face sample images to build baseline feature embeddings.

3. Start Live Tracking: Launch the recognition view from the web portal to open the camera stream.

4. Automatic Logging: As registered individuals appear in front of the camera, the system detects their faces, verifies their identity, and creates an attendance record with a timestamp in the database.

5. View Reports: Access the dashboard to view daily logs, filter by date, or review missing entries.
