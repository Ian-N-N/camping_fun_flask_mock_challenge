# ACCESS CAMP FLASK API
- This is a an API Backend for Access camp, designed to manage campers, activities and signups. It is built with **Flask**, **Flask-SQLAlchemy**, and **Flask-Migrate**, and follows the **MVC architecture**. I have also incorporated a simple home page to navigate to the endpoints easily

## Key API Features
- List, create, and update campers  
- List and delete activities  
- Create signups linking campers to activities  
- Validate inputs and return appropriate status codes 

## Folder Structure
```bash
CAMPING_FUN_FLASK_MOCK_CHALLENGE/
│
├── env/                        # Python virtual environment
│
├── server/
│   ├── __pycache__/            # Python cache files
│   ├── instance/
│   │   └── camp.db             # SQLite database
│   ├── migrations/
│   │   ├── __pycache__/        # Migration cache
│   │   └── versions/
│   │       └── 61da72213ce2_initial_model.py
│   ├── alembic.ini             # Alembic configuration
│   ├── env.py                  # Flask env or migration script
│   ├── script.py.mako          # Alembic template file
│   ├── app.py                  # Main Flask app
│   ├── db.py                   # DB initialization
│   ├── models.py               # SQLAlchemy models
│   └── seed.py                 # Seed database with Faker
│
├── README.md
├── requirements.txt
```
## Installation
```bash
git clone [repository-link]
cd camping_fun_flask_mock_challenge
```
### Create and activate virtual environment
```bash
python3 -m venv env
source env/bin/activate  # Linux / WSL
```
### Install dependencies
```bash
pip install -r server/requirements.txt
```
### Set Environment variables
```bash
$ export FLASK_APP=server/app.py
$ export FLASK_ENV=development
```
## Database setup
### Initialize migrations
```bash
cd server
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
```
### Seed database with fake data
```bash
flask seed
```
### Running the API
```bash
python server/app.py
```
## Author
Ian Ngoru Njuguna
