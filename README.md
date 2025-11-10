# ACCESS CAMPL FLASK API
- This is a an API Backend for Access camp, designed to manage campers, activities and signups. It is built with **Flask**, **Flask-SQLAlchemy**, and **Flask-Migrate**, and follows the **MVC architecture**.

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

