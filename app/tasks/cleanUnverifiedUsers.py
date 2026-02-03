from datetime import datetime, timedelta
from app.database import sessionLocal
from app.models import User
from app.celery import celeryApp

@celeryApp.task
def delete_unverified_users():
    db = sessionLocal()
    try:
        cutoff = datetime.now() - timedelta(days = 2)
        usersToDelete = db.query(User).filter(
            User.isVerified == False,
            User.createdAt < cutoff).all()
        
        counter = 0
        for u in usersToDelete: 
            db.delete(u)
            counter += 1

        db.commit()
        print(f"Deleted: {counter} unverified users")
        
    finally: db.close()