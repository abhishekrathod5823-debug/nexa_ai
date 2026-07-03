# test_db.py
# Yeh ek temporary file hai sirf database connection test karne ke liye

from app.database import engine
from app.models import Base

# Yeh connection test karega aur agar tables already nahi hain to bana dega
Base.metadata.create_all(bind=engine)

print("Connection successful! Tables verified.")