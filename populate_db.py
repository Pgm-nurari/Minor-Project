"""
Script to populate the FinSight database with dummy data
Run this script to add test data to your database
"""

import os
import sys
from datetime import date, time, datetime
from werkzeug.security import generate_password_hash

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.modules.models import (
    Department, Role, User, EventType, Event, SubEvent,
    TransactionNature, PaymentMode, TransactionCategory, AccountCategory,
    Transaction, TransactionItem, Budget
)

def clear_all_data():
    """Clear all existing data from the database"""
    print("Clearing existing data...")
    try:
        TransactionItem.query.delete()
        Transaction.query.delete()
        Budget.query.delete()
        SubEvent.query.delete()
        Event.query.delete()
        User.query.delete()
        Department.query.delete()
        Role.query.delete()
        EventType.query.delete()
        TransactionNature.query.delete()
        PaymentMode.query.delete()
        TransactionCategory.query.delete()
        AccountCategory.query.delete()
        db.session.commit()
        print("✓ Existing data cleared successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing data: {e}")
        raise

def populate_departments():
    """Insert departments"""
    print("\nInserting Departments...")
    departments = [
        Department(Dept_ID=1, Name='Computer Science'),
        Department(Dept_ID=2, Name='Commerce'),
        Department(Dept_ID=3, Name='Visual Media'),
        Department(Dept_ID=4, Name='Management'),
        Department(Dept_ID=5, Name='Engineering')
    ]
    db.session.bulk_save_objects(departments)
    db.session.commit()
    print(f"✓ Inserted {len(departments)} departments")

def populate_roles():
    """Insert roles"""
    print("\nInserting Roles...")
    roles = [
        Role(Role_ID=101, Role_Name='Admin'),
        Role(Role_ID=102, Role_Name='Event Manager'),
        Role(Role_ID=103, Role_Name='Finance Manager')
    ]
    db.session.bulk_save_objects(roles)
    db.session.commit()
    print(f"✓ Inserted {len(roles)} roles")

def populate_event_types():
    """Insert event types"""
    print("\nInserting Event Types...")
    event_types = [
        EventType(Event_Type_ID=1, Event_Type_Name='Conference'),
        EventType(Event_Type_ID=2, Event_Type_Name='Workshop'),
        EventType(Event_Type_ID=3, Event_Type_Name='Seminar'),
        EventType(Event_Type_ID=4, Event_Type_Name='Cultural Event'),
        EventType(Event_Type_ID=5, Event_Type_Name='Sports Event')
    ]
    db.session.bulk_save_objects(event_types)
    db.session.commit()
    print(f"✓ Inserted {len(event_types)} event types")

def populate_transaction_metadata():
    """Insert transaction natures, payment modes, categories"""
    print("\nInserting Transaction Metadata...")
    
    # Transaction Natures
    natures = [
        TransactionNature(Nature_ID=1, Nature_Name='Revenue'),
        TransactionNature(Nature_ID=2, Nature_Name='Expense')
    ]
    db.session.bulk_save_objects(natures)
    
    # Payment Modes
    modes = [
        PaymentMode(Mode_ID=1, Mode_Name='Cash'),
        PaymentMode(Mode_ID=2, Mode_Name='UPI'),
        PaymentMode(Mode_ID=3, Mode_Name='Credit Card'),
        PaymentMode(Mode_ID=4, Mode_Name='Debit Card'),
        PaymentMode(Mode_ID=5, Mode_Name='Bank Transfer'),
        PaymentMode(Mode_ID=6, Mode_Name='Cheque')
    ]
    db.session.bulk_save_objects(modes)
    
    # Transaction Categories
    trans_categories = [
        TransactionCategory(Transaction_Category_ID=1, Category_Name='Registration Fees'),
        TransactionCategory(Transaction_Category_ID=2, Category_Name='Sponsorship'),
        TransactionCategory(Transaction_Category_ID=3, Category_Name='Venue Rental'),
        TransactionCategory(Transaction_Category_ID=4, Category_Name='Equipment Rental'),
        TransactionCategory(Transaction_Category_ID=5, Category_Name='Marketing'),
        TransactionCategory(Transaction_Category_ID=6, Category_Name='Refreshments'),
        TransactionCategory(Transaction_Category_ID=7, Category_Name='Prizes'),
        TransactionCategory(Transaction_Category_ID=8, Category_Name='Staff Payments'),
        TransactionCategory(Transaction_Category_ID=9, Category_Name='Miscellaneous')
    ]
    db.session.bulk_save_objects(trans_categories)
    
    # Account Categories
    acc_categories = [
        AccountCategory(Account_Category_ID=1, Category_Name='Assets'),
        AccountCategory(Account_Category_ID=2, Category_Name='Liabilities'),
        AccountCategory(Account_Category_ID=3, Category_Name='Income'),
        AccountCategory(Account_Category_ID=4, Category_Name='Expenses'),
        AccountCategory(Account_Category_ID=5, Category_Name='Equity')
    ]
    db.session.bulk_save_objects(acc_categories)
    
    db.session.commit()
    print("✓ Inserted transaction metadata")

def populate_users():
    """Insert users with hashed passwords"""
    print("\nInserting Users...")
    
    # Generate hashed password for 'Password@123'
    hashed_password = generate_password_hash('Password@123')
    
    users = [
        User(Username='Admin User', Email='admin@finsight.com', Password=hashed_password, 
             Role=101, Dept_ID=1, Verified=1),
        User(Username='John Doe', Email='john.doe@finsight.com', Password=hashed_password, 
             Role=102, Dept_ID=1, Verified=1),
        User(Username='Jane Smith', Email='jane.smith@finsight.com', Password=hashed_password, 
             Role=103, Dept_ID=2, Verified=1),
        User(Username='Mike Johnson', Email='mike.johnson@finsight.com', Password=hashed_password, 
             Role=102, Dept_ID=3, Verified=1),
        User(Username='Sarah Williams', Email='sarah.williams@finsight.com', Password=hashed_password, 
             Role=103, Dept_ID=4, Verified=1),
        User(Username='David Brown', Email='david.brown@finsight.com', Password=hashed_password, 
             Role=102, Dept_ID=5, Verified=1),
        User(Username='Emily Davis', Email='emily.davis@finsight.com', Password=hashed_password, 
             Role=103, Dept_ID=1, Verified=1),
        User(Username='Chris Wilson', Email='chris.wilson@finsight.com', Password=hashed_password, 
             Role=102, Dept_ID=2, Verified=0)
    ]
    
    for user in users:
        db.session.add(user)
    
    db.session.commit()
    print(f"✓ Inserted {len(users)} users (Password: Password@123)")

def populate_events():
    """Insert events"""
    print("\nInserting Events...")
    events = [
        Event(Finance_Manager=3, Event_Manager=2, Name='Tech Summit 2025', 
              Event_Type_ID=1, Date=date(2025, 1, 15), Days=2, Dept_ID=1),
        Event(Finance_Manager=5, Event_Manager=4, Name='Photography Workshop', 
              Event_Type_ID=2, Date=date(2025, 2, 20), Days=1, Dept_ID=3),
        Event(Finance_Manager=7, Event_Manager=6, Name='Innovation Conference', 
              Event_Type_ID=1, Date=date(2025, 3, 10), Days=3, Dept_ID=5),
        Event(Finance_Manager=3, Event_Manager=2, Name='AI & ML Seminar', 
              Event_Type_ID=3, Date=date(2024, 12, 1), Days=1, Dept_ID=1),
        Event(Finance_Manager=5, Event_Manager=4, Name='Cultural Fest 2025', 
              Event_Type_ID=4, Date=date(2025, 4, 15), Days=5, Dept_ID=3)
    ]
    
    for event in events:
        db.session.add(event)
    
    db.session.commit()
    print(f"✓ Inserted {len(events)} events")

def populate_sub_events():
    """Insert sub-events"""
    print("\nInserting Sub-Events...")
    sub_events = [
        SubEvent(Sub_Event_Manager=2, Name='Keynote Speech', Event_Type_ID=3, 
                Date=date(2025, 1, 15), Time=time(9, 0), Dept_ID=1, Event_ID=1),
        SubEvent(Sub_Event_Manager=2, Name='Panel Discussion', Event_Type_ID=3, 
                Date=date(2025, 1, 15), Time=time(14, 0), Dept_ID=1, Event_ID=1),
        SubEvent(Sub_Event_Manager=4, Name='Basic Photography', Event_Type_ID=2, 
                Date=date(2025, 2, 20), Time=time(10, 0), Dept_ID=3, Event_ID=2),
        SubEvent(Sub_Event_Manager=4, Name='Advanced Editing', Event_Type_ID=2, 
                Date=date(2025, 2, 20), Time=time(15, 0), Dept_ID=3, Event_ID=2),
        SubEvent(Sub_Event_Manager=6, Name='Startup Pitches', Event_Type_ID=1, 
                Date=date(2025, 3, 10), Time=time(11, 0), Dept_ID=5, Event_ID=3)
    ]
    
    for sub_event in sub_events:
        db.session.add(sub_event)
    
    db.session.commit()
    print(f"✓ Inserted {len(sub_events)} sub-events")

def populate_budgets():
    """Insert budgets"""
    print("\nInserting Budgets...")
    budgets = [
        Budget(Amount=150000.00, Notes='Total budget for Tech Summit', Event_ID=1, Sub_Event_ID=None),
        Budget(Amount=50000.00, Notes='Budget for Photography Workshop', Event_ID=2, Sub_Event_ID=None),
        Budget(Amount=200000.00, Notes='Innovation Conference Budget', Event_ID=3, Sub_Event_ID=None),
        Budget(Amount=30000.00, Notes='Budget for keynote speaker', Event_ID=None, Sub_Event_ID=1),
        Budget(Amount=20000.00, Notes='Panel discussion expenses', Event_ID=None, Sub_Event_ID=2)
    ]
    
    db.session.bulk_save_objects(budgets)
    db.session.commit()
    print(f"✓ Inserted {len(budgets)} budgets")

def populate_transactions():
    """Insert transactions and transaction items"""
    print("\nInserting Transactions...")
    
    # Transactions for Event 1 (Tech Summit)
    t1 = Transaction(User_ID=2, Event_ID=1, Sub_Event_ID=None, Bill_No='INV001', 
                    Party_Name='Tech Corp Sponsorship', Nature_ID=1, Mode_ID=5, 
                    Date=date(2024, 12, 15), Transaction_Category_ID=2, Account_Category_ID=3)
    db.session.add(t1)
    db.session.flush()
    
    items_t1 = [
        TransactionItem(Transaction_ID=t1.Transaction_ID, Description='Gold Sponsorship Package', Amount=50000.00)
    ]
    
    t2 = Transaction(User_ID=2, Event_ID=1, Sub_Event_ID=None, Bill_No='INV002', 
                    Party_Name='Student Registrations', Nature_ID=1, Mode_ID=2, 
                    Date=date(2024, 12, 20), Transaction_Category_ID=1, Account_Category_ID=3)
    db.session.add(t2)
    db.session.flush()
    
    items_t2 = [
        TransactionItem(Transaction_ID=t2.Transaction_ID, Description='Early Bird Registrations (50 students)', Amount=25000.00),
        TransactionItem(Transaction_ID=t2.Transaction_ID, Description='Regular Registrations (30 students)', Amount=18000.00)
    ]
    
    t3 = Transaction(User_ID=2, Event_ID=1, Sub_Event_ID=None, Bill_No='BILL001', 
                    Party_Name='Convention Center', Nature_ID=2, Mode_ID=6, 
                    Date=date(2024, 12, 10), Transaction_Category_ID=3, Account_Category_ID=4)
    db.session.add(t3)
    db.session.flush()
    
    items_t3 = [
        TransactionItem(Transaction_ID=t3.Transaction_ID, Description='Venue rental for 2 days', Amount=35000.00),
        TransactionItem(Transaction_ID=t3.Transaction_ID, Description='Audio/Visual equipment', Amount=15000.00)
    ]
    
    t4 = Transaction(User_ID=2, Event_ID=1, Sub_Event_ID=1, Bill_No='BILL002', 
                    Party_Name='Dr. Smith (Speaker)', Nature_ID=2, Mode_ID=5, 
                    Date=date(2024, 12, 12), Transaction_Category_ID=8, Account_Category_ID=4)
    db.session.add(t4)
    db.session.flush()
    
    items_t4 = [
        TransactionItem(Transaction_ID=t4.Transaction_ID, Description='Keynote speaker fee', Amount=25000.00),
        TransactionItem(Transaction_ID=t4.Transaction_ID, Description='Travel and accommodation', Amount=8000.00)
    ]
    
    t5 = Transaction(User_ID=2, Event_ID=1, Sub_Event_ID=None, Bill_No='BILL003', 
                    Party_Name='Marketing Agency', Nature_ID=2, Mode_ID=3, 
                    Date=date(2024, 12, 18), Transaction_Category_ID=5, Account_Category_ID=4)
    db.session.add(t5)
    db.session.flush()
    
    items_t5 = [
        TransactionItem(Transaction_ID=t5.Transaction_ID, Description='Social media campaign', Amount=12000.00),
        TransactionItem(Transaction_ID=t5.Transaction_ID, Description='Print materials', Amount=5000.00)
    ]
    
    # Transactions for Event 2 (Photography Workshop)
    t6 = Transaction(User_ID=4, Event_ID=2, Sub_Event_ID=None, Bill_No='INV003', 
                    Party_Name='Workshop Registration Fees', Nature_ID=1, Mode_ID=2, 
                    Date=date(2025, 1, 10), Transaction_Category_ID=1, Account_Category_ID=3)
    db.session.add(t6)
    db.session.flush()
    
    items_t6 = [
        TransactionItem(Transaction_ID=t6.Transaction_ID, Description='Workshop registration (20 participants)', Amount=30000.00)
    ]
    
    t7 = Transaction(User_ID=4, Event_ID=2, Sub_Event_ID=None, Bill_No='BILL004', 
                    Party_Name='Camera Equipment Rental', Nature_ID=2, Mode_ID=1, 
                    Date=date(2025, 1, 15), Transaction_Category_ID=4, Account_Category_ID=4)
    db.session.add(t7)
    db.session.flush()
    
    items_t7 = [
        TransactionItem(Transaction_ID=t7.Transaction_ID, Description='DSLR cameras (5 units)', Amount=8000.00),
        TransactionItem(Transaction_ID=t7.Transaction_ID, Description='Lighting equipment', Amount=4000.00)
    ]
    
    t8 = Transaction(User_ID=4, Event_ID=2, Sub_Event_ID=3, Bill_No='BILL005', 
                    Party_Name='Professional Photographer Fee', Nature_ID=2, Mode_ID=5, 
                    Date=date(2025, 2, 18), Transaction_Category_ID=8, Account_Category_ID=4)
    db.session.add(t8)
    db.session.flush()
    
    items_t8 = [
        TransactionItem(Transaction_ID=t8.Transaction_ID, Description='Workshop instructor fee', Amount=15000.00)
    ]
    
    # Transactions for Event 4 (Completed - AI & ML Seminar)
    t9 = Transaction(User_ID=2, Event_ID=4, Sub_Event_ID=None, Bill_No='INV004', 
                    Party_Name='Seminar Registrations', Nature_ID=1, Mode_ID=2, 
                    Date=date(2024, 11, 15), Transaction_Category_ID=1, Account_Category_ID=3)
    db.session.add(t9)
    db.session.flush()
    
    items_t9 = [
        TransactionItem(Transaction_ID=t9.Transaction_ID, Description='Student registrations (40 students)', Amount=20000.00)
    ]
    
    t10 = Transaction(User_ID=2, Event_ID=4, Sub_Event_ID=None, Bill_No='BILL006', 
                     Party_Name='Seminar Hall Booking', Nature_ID=2, Mode_ID=5, 
                     Date=date(2024, 11, 20), Transaction_Category_ID=3, Account_Category_ID=4)
    db.session.add(t10)
    db.session.flush()
    
    items_t10 = [
        TransactionItem(Transaction_ID=t10.Transaction_ID, Description='Seminar hall for 1 day', Amount=8000.00)
    ]
    
    t11 = Transaction(User_ID=2, Event_ID=4, Sub_Event_ID=None, Bill_No='BILL007', 
                     Party_Name='Refreshments', Nature_ID=2, Mode_ID=1, 
                     Date=date(2024, 12, 1), Transaction_Category_ID=6, Account_Category_ID=4)
    db.session.add(t11)
    db.session.flush()
    
    items_t11 = [
        TransactionItem(Transaction_ID=t11.Transaction_ID, Description='Tea and snacks for 50 people', Amount=3500.00)
    ]
    
    t12 = Transaction(User_ID=2, Event_ID=4, Sub_Event_ID=None, Bill_No='BILL008', 
                     Party_Name='Certificates Printing', Nature_ID=2, Mode_ID=1, 
                     Date=date(2024, 11, 25), Transaction_Category_ID=9, Account_Category_ID=4)
    db.session.add(t12)
    db.session.flush()
    
    items_t12 = [
        TransactionItem(Transaction_ID=t12.Transaction_ID, Description='Participation certificates (50 pcs)', Amount=2000.00)
    ]
    
    # Add all transaction items
    all_items = items_t1 + items_t2 + items_t3 + items_t4 + items_t5 + items_t6 + items_t7 + items_t8 + items_t9 + items_t10 + items_t11 + items_t12
    for item in all_items:
        db.session.add(item)
    
    db.session.commit()
    print(f"✓ Inserted 12 transactions with {len(all_items)} transaction items")

def print_summary():
    """Print summary of inserted data"""
    print("\n" + "="*60)
    print("DATABASE POPULATION SUMMARY")
    print("="*60)
    print(f"Departments:            {Department.query.count()}")
    print(f"Roles:                  {Role.query.count()}")
    print(f"Event Types:            {EventType.query.count()}")
    print(f"Users:                  {User.query.count()}")
    print(f"Events:                 {Event.query.count()}")
    print(f"Sub-Events:             {SubEvent.query.count()}")
    print(f"Budgets:                {Budget.query.count()}")
    print(f"Transactions:           {Transaction.query.count()}")
    print(f"Transaction Items:      {TransactionItem.query.count()}")
    print(f"Transaction Natures:    {TransactionNature.query.count()}")
    print(f"Payment Modes:          {PaymentMode.query.count()}")
    print(f"Transaction Categories: {TransactionCategory.query.count()}")
    print(f"Account Categories:     {AccountCategory.query.count()}")
    print("="*60)
    print("\n✓ Database populated successfully!")
    print("\nTEST CREDENTIALS:")
    print("  Email: john.doe@finsight.com (Event Manager)")
    print("  Email: jane.smith@finsight.com (Finance Manager)")
    print("  Email: admin@finsight.com (Admin)")
    print("  Password: Password@123")
    print("="*60)

def main():
    """Main function to populate database"""
    print("="*60)
    print("FINSIGHT DATABASE POPULATION SCRIPT")
    print("="*60)
    
    app = create_app('development')
    
    with app.app_context():
        try:
            # Clear existing data
            clear_all_data()
            
            # Populate tables in order
            populate_departments()
            populate_roles()
            populate_event_types()
            populate_transaction_metadata()
            populate_users()
            populate_events()
            populate_sub_events()
            populate_budgets()
            populate_transactions()
            
            # Print summary
            print_summary()
            
        except Exception as e:
            print(f"\n✗ Error during population: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()
