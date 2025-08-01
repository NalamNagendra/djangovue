# A simple Movie & Social Posts App

A full-stack application with a Django REST API backend and Vue.js frontend.

## Quick Start

### Backend Setup

```sh
# Navigate to backend
cd backend_repo

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
