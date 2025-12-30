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
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
from .modules.transaction_utils import *

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

        # Fetch category and mode totals with names
        category_totals = {}
        for category_id in get_all_transaction_category_ids():
            category_name = get_category_name(category_id)  # Fetch the name for the category ID
            category_totals[category_name] = get_category_total(event_id, category_id)

        mode_totals = {}
        for mode_id in get_all_payment_mode_ids():
            mode_name = get_mode_name(mode_id)  # Fetch the name for the mode ID
            mode_totals[mode_name] = get_mode_total(event_id, mode_id)

        # Fetch event details for the selected event (name, date, etc.)
        event_details = get_event_details(event_id)

        # Render the template with calculated data
        return render_template(
            'finance_manager/event_details.html',
            event_id=event_id,
            user_id=user_id,
            revenue=revenue,
            expenses=expenses,
            category_totals=category_totals,
            mode_totals=mode_totals,
            event_details=event_details  # Pass event details to the template
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

def get_event_details(event_id):
    """Fetch details of an event based on Event ID."""
    event = Event.query.filter_by(Event_ID=event_id).first()
    if event:
        # Fetch related department and event type names from their respective models
        department_name = event.department.Name if event.department else "Unknown Department"
        event_type_name = event.event_type.Event_Type_Name if event.event_type else "Unknown Event Type"
        
        # Fetch finance and event managers' names
        finance_manager_name = event.finance_manager.Username if event.finance_manager else "No Finance Manager"
        event_manager_name = event.event_manager.Username if event.event_manager else "No Event Manager"

        return {
            "id": event_id,
            "name": event.Name,                     # Event Name
            "date": event.Date,                     # Event Date
            "department": department_name,          # Department Name
            "event_type": event_type_name,          # Event Type Name
            "days": event.Days,                     # Event Days
            "finance_manager": finance_manager_name,  # Finance Manager Name
            "event_manager": event_manager_name     # Event Manager Name
        }
    return {}


@finance_manager_bp.route('/event_visualization/<int:event_id>')
def event_visualization(user_id, event_id):
    try:
        event_name = get_event_name(event_id)
        print(event_name)
        
        # Fetch revenue and expense data
        revenue = get_revenue_total(event_id)
        expense = get_expense_total(event_id)

        # Fetch category totals
        categories = get_all_transaction_category_ids()
        category_totals = []
        for category_id in categories:
            category_total = get_category_total(event_id, category_id)
            if category_total > 0:
                category_name = get_category_name(category_id)
                category_totals.append({'name': category_name, 'total': category_total})
                
        # print(category_totals)

        # Fetch mode totals
        modes = get_all_payment_mode_ids()
        mode_totals = []
        for mode_id in modes:
            mode_total = get_mode_total(event_id, mode_id)
            if mode_total > 0:
                mode_name = get_mode_name(mode_id)
                mode_totals.append({'name': mode_name, 'total': mode_total})

        # Generate Pie Chart JSON (avoid issues with empty data)
        if category_totals:
            category_fig = px.pie(
                names=[cat['name'] for cat in category_totals],
                values=[cat['total'] for cat in category_totals],
                title='Transaction Totals by Category'
            ).to_json()
        else:
            category_fig = None

        if mode_totals:
            mode_fig = px.pie(
                names=[mode['name'] for mode in mode_totals],
                values=[mode['total'] for mode in mode_totals],
                title='Transaction Totals by Payment Mode'
            ).to_json()
        else:
            mode_fig = None

        # Revenue vs Expense Bar Chart
        revenue_expense_fig = go.Figure()
        revenue_expense_fig.add_trace(go.Bar(x=['Revenue', 'Expenses'], y=[revenue, expense]))
        revenue_expense_fig.update_layout(title='Revenue vs Expenses', xaxis_title='Type', yaxis_title='Amount (₹)', template='plotly_dark')
        revenue_expense_fig_json = revenue_expense_fig.to_json()

        # Render template
        return render_template(
            'finance_manager/event_visualization.html',
            revenue_expense_fig=revenue_expense_fig_json,
            category_fig=category_fig,
            mode_fig=mode_fig,
            user_id=user_id,
            event_id=event_id,
            event_name=event_name,
        )
    except Exception as e:
        print(f"Error in visualization: {e}")
        return redirect(url_for('finance_manager.view_events', user_id=user_id))
    
def get_event_name(event_id):
    event = db.session.query(Event).filter_by(Event_ID=event_id).first()
    return event.Name if event else "Unknown Event"    
