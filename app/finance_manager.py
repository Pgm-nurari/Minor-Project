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
    return render_template('finance_manager/event_details.html', event_id=event_id, user_id=user_id)

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

@finance_manager_bp.route('/event_details/<int:event_id>/visualizations')
def event_finance_visualizations(user_id, event_id):
    try:
        # Fetch transactions related to the event
        transactions = (
            db.session.query(Transaction)
            .filter(Transaction.Event_ID == event_id)
            .options(
                joinedload(Transaction.transaction_nature),
                joinedload(Transaction.payment_mode),
                joinedload(Transaction.transaction_category)
            )
            .all()
        )
        
        # Fetch budget details
        budget = db.session.query(Budget).filter(Budget.Event_ID == event_id).first()

        # Prepare data for visualizations
        payment_mode_data = defaultdict(float)
        transaction_category_data = defaultdict(float)

        for txn in transactions:
            payment_mode_data[txn.payment_mode.Mode_Name] += txn.Amount
            transaction_category_data[txn.transaction_category.Name] += txn.Amount

        allocated_budget = budget.Amount if budget else 0
        utilized_budget = sum(txn.Amount for txn in transactions)

        # Create visualizations
        plots = {}

        # 1. Bar chart for transactions by payment mode
        plt.figure(figsize=(8, 5))
        plt.bar(payment_mode_data.keys(), payment_mode_data.values(), color='skyblue')
        plt.title("Transactions by Payment Mode")
        plt.xlabel("Payment Modes")
        plt.ylabel("Amount")
        plots['payment_mode'] = save_plot()

        # 2. Pie chart for transactions by category
        plt.figure(figsize=(7, 7))
        plt.pie(
            transaction_category_data.values(),
            labels=transaction_category_data.keys(),
            autopct='%1.1f%%',
            startangle=140
        )
        plt.title("Transactions by Category")
        plots['transaction_category'] = save_plot()

        # 3. Budget Allocation vs Utilization
        plt.figure(figsize=(6, 4))
        plt.bar(['Allocated Budget', 'Utilized Budget'], [allocated_budget, utilized_budget], color=['green', 'orange'])
        plt.title("Budget Allocation vs Utilization")
        plots['budget_comparison'] = save_plot()

        return render_template(
            'finance_manager/event_visualizations.html',
            event_id=event_id,
            plots=plots,
            user_id=user_id
        )
    except SQLAlchemyError as e:
        print("Error creating visualizations:", e)
        flash("Error generating visualizations.")
        return redirect(url_for('finance_manager.event_details', user_id=user_id, event_id=event_id))

def save_plot():
    """Helper function to save the plot as a base64 image."""
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return f"data:image/png;base64,{plot_url}"

def save_plot():
    """Helper function to save the plot as a base64 image."""
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return f"data:image/png;base64,{plot_url}"