from app import app, db, User, Notification, Post, Event, EventRegistration,Job,JobApplication

def seed():
    with app.app_context():
        print(">>> Wiping old data...")
        db.drop_all()
        db.create_all()
        
        print(">>> Creating new data...")
        # 1. User
        student = User(username='Syed', password='123', role='Student')
        db.session.add(student)
        db.session.commit()

        # 2. Notifications & Posts
        notifs = [Notification(title="Miracle Rosser", message="Hey!", user_id=student.id)]
        posts = [Post(content="Hello World!", author_name="Syed")]
        print(">>> Wiping old data...")
        db.drop_all()
        db.create_all()
        
        print(">>> Creating Users...")
        # 1. The Student (You)
        syed = User(username='Syed', password='123', role='Student')
        
        # 2. The Alumni (Mentors)
        alum1 = User(username='Dr. Sarah', password='123', role='Alumni')
        alum2 = User(username='Mr. James', password='123', role='Alumni')
        alum3 = User(username='Ms. Fiona', password='123', role='Alumni')

        db.session.add_all([syed, alum1, alum2, alum3])
        db.session.commit()
        
        print(">>> Success! Login as Syed (123) and go to Mentorship page.")
        # 3. Events (NEW)
        # In seed_data.py, update the events list:
        events = [
            Event(
                title="MMU Career Fair 2026", 
                location="Grand Hall", 
                date_str="MAR 15", 
                time_str="10:00 AM - 4:00 PM",
                description="Join us for the biggest career fair of the year! Meet recruiters from top tech companies like Google, Grab, and Petronas. Bring your CV and dress professionally."
            ),
            Event(
                title="Alumni Networking Dinner", 
                location="Tamarind Square", 
                date_str="APR 02", 
                time_str="7:00 PM - 10:00 PM",
                description="A casual night to reconnect with old friends and make new connections. Buffet dinner included. Ticket price: RM50 (Free for registered alumni)."
            ),
            Event(
                title="Hackathon Kickoff", 
                location="FCI Lab 3", 
                date_str="MAY 10", 
                time_str="9:00 AM",
                description="The theme for this year's hackathon is AI for Good. Form a team of 3-4 and build a solution in 24 hours. Great prizes to be won!"
            )
        ]
        jobs = [
            Job(
                title="Junior Software Engineer", 
                company="Grab Malaysia", 
                location="Kuala Lumpur", 
                job_type="Full-time",
                description="We are looking for a fresh grad with Python and React experience."
            ),
            Job(
                title="Data Analyst Intern", 
                company="Maybank", 
                location="Menara Maybank, KL", 
                job_type="Internship",
                description="Join our Digital Banking team. SQL knowledge is required."
            ),
            Job(
                title="Frontend Developer", 
                company="Shopee", 
                location="Mid Valley, KL", 
                job_type="Full-time",
                description="Experience with Vue.js or React is preferred."
            ),
            Job(
                title="IT Support Executive", 
                company="Multimedia University", 
                location="Cyberjaya", 
                job_type="Contract",
                description="Support campus IT infrastructure."
            )
        ]
        
        db.session.add_all(notifs)
        db.session.add_all(posts)
        db.session.add_all(events)
        db.session.add_all(jobs)
        db.session.commit()

        
        print(">>> Success! Database ready.")

if __name__ == '__main__':
    seed()