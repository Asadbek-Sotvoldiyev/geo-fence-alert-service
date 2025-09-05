## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Git

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/geo-fence-service.git
cd geo-fence-service
```

### 2. Create virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=geofence_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
```

### 5. Setup PostgreSQL database
```bash
# Create database
createdb geofence_db

# Or using psql:
psql -c "CREATE DATABASE geofence_db;"
```

### 6. Run migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Start the services

#### Terminal 1: Django server
```bash
python manage.py runserver
```

#### Terminal 2: Celery worker
```bash
celery -A config worker --loglevel=info
```

### 8. Access the application
- **API**: http://localhost:8000/api/swagger/
- **Admin Panel**: http://localhost:8000/admin/

