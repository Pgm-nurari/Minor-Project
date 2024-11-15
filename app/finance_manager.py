from flask import Blueprint, render_template, redirect, request, flash, url_for, get_flashed_messages, session  
from .modules.models import Transaction, TransactionNature, PaymentMode, TransactionCategory, AccountCategory
from app import db
from .modules.models import *
from .modules.db_queries import *
from sqlalchemy.orm import joinedload, validates
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict
from sqlalchemy import func
from datetime import datetime, date
from .test_data import test_user_data, test_event_data

finance_manager_bp = Blueprint('finance_manager', __name__, url_prefix='/finmng/<int:user_id>')

@finance_manager_bp.route('/dashboard')
def finance_manager(user_id):
    events = get_events(user_id)
    return render_template('finance_manager/financemanager_dashboard.html', events=events, user=test_user_data)

@finance_manager_bp.route('/view_events')
def view_events(user_id):
    events = get_events(user_id)
    return render_template('finance_manager/view_events.html', events=events, user_id=user_id)

@finance_manager_bp.route('/event_details/<int:event_id>')
def event_details(user_id, event_id):
    pass

def get_events(user_id):
    try:
        # Fetch events where the event_manager matches the user_id, with necessary joins
        events = (
            db.session.query(Event)
            .filter(Event.Finance_Manager == user_id)
            .options(
                joinedload(Event.department),
                joinedload(Event.event_type),
                joinedload(Event.finance_manager)
            )
            .all()
        )

        # Helper function to determine the event status
        def determine_status(event_date):
            today = date.today()
            if event_date > today:
                return "Upcoming"
            elif event_date == today:
                return "Ongoing"
            else:
                return "Completed"

        # Group events by status using defaultdict
        grouped_events = defaultdict(list)

        # Process events into the required dictionary structure
        for event in events:
            status = determine_status(event.Date)
            grouped_events[status].append({
                "id": event.Event_ID,
                "event_name": event.Name,
                "status": status,  # Status based on event date
                "type": event.event_type.Event_Type_Name,  # Name from EventType model
                "department": event.department.Name,  # Name from Department model
                "date": event.Date
            })

        # Convert defaultdict to regular dict for clean return
        return dict(grouped_events)

    except SQLAlchemyError as e:
        print("Error fetching events:", e)
        return {}

def get_transactions_of_event(event_id):
    """
    Get the transactions as a list of dictionaries for a given event.
    Each row will have the following keys: transaction_id, amount, transaction_nature, payment_mode,
    date, bill_no, party_name, transaction_category, and account_category.
    The event_id in transaction table refers to the event_id in the event table.
    This function joins the transaction table with other related foreign key tables.
    """
    pass

def get_budget(event_id):
    """
    Here, the budget will be gained for the respective events.
    The event_id will be checked in both the event_id and the sub_event_id. columns of the budget table.
    """
    
    
    pass
