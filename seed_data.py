from app import app, db, User, Notification, Post, Event, Job, EventRegistration, JobApplication, Mentorship, EventFeedback

def seed():
    with app.app_context():
        print(">>> Wiping old data...")
        db.drop_all()
        db.create_all()
        
        print(">>> Creating Users...")
        # 1. The Student (You)
        syed = User(
            username='Syed', 
            password='123', 
            role='Student',
            full_name='Syed Ali',
            email='syed@example.com',
            headline='Software Engineering Student',
            bio='Aspiring Full Stack Developer passionate about Python and Flask.',
            location='Cyberjaya',
            skills='Python, HTML, CSS, Flask'
        )
        
        # 2. The Alumni (Mentors)
        alum1 = User(
            username='Dr. Sarah', 
            password='123', 
            role='Alumni',
            full_name='Dr. Sarah Ahmed',
            headline='Senior Data Scientist at Google',
            bio='Ph.D. in AI. Helping students navigate the world of Data Science.',
            location='Singapore',
            skills='AI, Machine Learning, Data Science'
        )
        
        alum2 = User(
            username='Mr. James', 
            password='123', 
            role='Alumni',
            full_name='James Lee',
            headline='Product Manager at Grab',
            location='Kuala Lumpur'
        )
        
        alum3 = User(
            username='Ms. Fiona', 
            password='123', 
            role='Alumni',
            full_name='Fiona Tan',
            headline='Software Engineer at Shopee',
            location='Singapore'
        )

        db.session.add_all([syed, alum1, alum2, alum3])
        db.session.commit()

        print(">>> Creating Content...")
        
        # 3. Notifications & Posts
        notifs = [Notification(title="Welcome!", message="Welcome to the Alumni Network.", user_id=syed.id)]
        posts = [
            Post(content="Just finished my final year project! #MMU #Graduation", author_name="Syed"),
            Post(content="Looking for interns at Grab! DM me for details.", author_name="Mr. James")
        ]

        # 4. Events
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

        # 5. Jobs
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

        print(">>> Success! Database seeded.")
        print(">>> Login with Username: 'Syed' and Password: '123'")

if __name__ == '__main__':
    seed()