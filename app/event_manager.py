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

event_manager_bp = Blueprint('event_manager', __name__, url_prefix='/evemng/<int:user_id>')

@event_manager_bp.route('/')
def event_manager(user_id):
    events = get_events(user_id)
    return render_template('event_manager/eventmanager_dash.html', events=events, user_id=user_id)

@event_manager_bp.route('/view_events')
def view_events(user_id):
    events = get_events(user_id)
    return render_template('event_manager/view_events.html', events=events, user_id=user_id)

@event_manager_bp.route('/event_details/<int:event_id>')
def event_details(user_id, event_id):
    try:
        # First, try to retrieve the event from the Event table
        event = db.session.query(Event).filter_by(Event_ID=event_id, Event_Manager=user_id).first()

        # If not found in Event, try to find it in SubEvent
        if not event:
            event = db.session.query(SubEvent).filter_by(Sub_Event_ID=event_id, Sub_Event_Manager=user_id).first()

        # If still not found, flash a message and redirect
        if not event:
            flash("Event not found or you don't have access to view it.", "danger")
            return redirect(url_for('event_manager.event_manager', user_id=user_id))

        # Prepare context for rendering, based on whether it's Event or SubEvent
        event_data = [{
            "id": event.Event_ID if isinstance(event, Event) else event.Sub_Event_ID,
            "event_name": event.Name,
            "status": "Ongoing" if event.Date == date.today() else "Completed" if event.Date < date.today() else "Upcoming",
            "type": event.event_type.Event_Type_Name,
            "department": event.department.Name,
            "date": event.Date
        }]

        # Render event details page with the event data
        return render_template('event_manager/event_details.html', events=event_data, user_id=user_id)

    except SQLAlchemyError as e:
        flash("An error occurred while fetching the event details.", "danger")
        print("Error fetching event details:", e)
        return redirect(url_for('event_manager.event_manager', user_id=user_id))

@event_manager_bp.route('/transaction_form/<int:event_id>', methods=['GET', 'POST'])
def transaction_form(user_id, event_id):
    # Render the form with the lookup data
    return render_template('event_manager/transaction_form.html', event_id=event_id, user_id=user_id,)

def get_events(user_id):
    try:
        # Fetch events where the event_manager matches the user_id, with necessary joins
        events = (
            db.session.query(Event)
            .filter(Event.Event_Manager == user_id)
            .options(
                joinedload(Event.department),
                joinedload(Event.event_type),
                joinedload(Event.event_manager)
            )
            .all()
        )

        # Fetch sub-events where the sub_event_manager matches the user_id, with necessary joins
        sub_events = (
            db.session.query(SubEvent)
            .join(Event)
            .filter(SubEvent.Sub_Event_Manager == user_id)
            .options(
                joinedload(SubEvent.department),
                joinedload(SubEvent.event_type),
                joinedload(SubEvent.sub_event_manager)
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

        # Process sub-events similarly
        for sub_event in sub_events:
            status = determine_status(sub_event.Date)
            grouped_events[status].append({
                "id": sub_event.Sub_Event_ID,
                "event_name": sub_event.Name,
                "status": status,  # Status based on sub-event date
                "type": sub_event.event_type.Event_Type_Name,  # Name from EventType model
                "department": sub_event.department.Name,  # Name from Department model
                "date": sub_event.Date
            })

        # Convert defaultdict to regular dict for clean return
        return dict(grouped_events)

    except SQLAlchemyError as e:
        print("Error fetching events:", e)
        return {}

def get_all_transactions(user_id):
    pass

def get_transactions_of_event(event_id):
    """
    Get the transactions as a list of dictionaries for a given event.
    Each row will have the following keys: transaction_id, amount, transaction_nature, payment_mode,
    date, bill_no, party_name, transaction_category, and account_category.
    This function joins the transaction table with other related foreign key tables.
    """
    pass

def get_budget(event_id):
    """
    Here, the budget will be gained for the respective events.
    The event_id will be checked in both the event_id and the sub_event_id. columns of the budget table.
    """
    
    
    pass
