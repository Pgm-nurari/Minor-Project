from flask import Blueprint, render_template, redirect, request, flash, url_for, get_flashed_messages, session  
from .modules.models import Transaction, TransactionNature, PaymentMode, TransactionCategory, AccountCategory
from app import db
from .modules.models import *
from .modules.db_queries import *
from sqlalchemy.orm import joinedload, validates
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict
from sqlalchemy import func
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime, date
from .test_data import test_user_data, test_event_data
from .modules.transaction_utils import (
    get_revenue_total,
    get_expense_total,
    get_category_total,
    get_mode_total,
    get_transaction_ids,
    get_all_transaction_category_ids,
    get_all_payment_mode_ids
)

finance_manager_bp = Blueprint('finance_manager', __name__, url_prefix='/finmng/<int:user_id>')

@finance_manager_bp.route('/')
def finance_manager(user_id):
    events = get_events(user_id)
    return render_template('finance_manager/financemanager_dashboard.html', events=events, user=test_user_data, user_id=user_id)

@finance_manager_bp.route('/view_events')
def view_events(user_id):
    events = get_events(user_id)
    return render_template('finance_manager/view_events.html', events=events, user_id=user_id)    

@finance_manager_bp.route('/event_details/<int:event_id>')
def event_details(user_id, event_id):
    try:
        # Fetch transaction IDs for the given event
        transaction_ids = get_transaction_ids(event_id)
        print(transaction_ids)

        # Ensure transaction_ids is a list
        if not transaction_ids:
            transaction_ids = []

        # Calculate revenue and expenses
        revenue = get_revenue_total(event_id)
        expenses = get_expense_total(event_id)

        # Fetch category and mode totals
        category_totals = {
            category_id: get_category_total(event_id, category_id)
            for category_id in get_all_transaction_category_ids()
        }
        mode_totals = {
            mode_id: get_mode_total(event_id, mode_id)
            for mode_id in get_all_payment_mode_ids()
        }

        # Render the template with calculated data
        return render_template(
            'finance_manager/event_details.html',
            event_id=event_id,
            user_id=user_id,
            revenue=revenue,
            expenses=expenses,
            category_totals=category_totals,
            mode_totals=mode_totals
        )
    except Exception as e:
        print(f"Error fetching event details: {e}")
        return redirect(url_for('finance_manager.view_events', user_id=user_id))

# Fetch Events Helper Function
def get_events(user_id):
    try:
        # Fetch events for the finance manager
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

        # Group events by their status
        grouped_events = defaultdict(list)
        for event in events:
            status = determine_status(event.Date)
            grouped_events[status].append({
                "id": event.Event_ID,
                "event_name": event.Name,
                "status": status,
                "type": event.event_type.Event_Type_Name,
                "department": event.department.Name,
                "date": event.Date
            })

        return dict(grouped_events)

    except SQLAlchemyError as e:
        print("Error fetching events:", e)
        return {}

# Helper Function: Determine Event Status
def determine_status(event_date):
    today = date.today()
    if event_date > today:
        return "Upcoming"
    elif event_date == today:
        return "Ongoing"
    else:
        return "Completed"

