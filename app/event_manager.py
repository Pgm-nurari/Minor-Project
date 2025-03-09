from flask import Blueprint, render_template, redirect, request, flash, url_for, get_flashed_messages, session  
from app import db
import json
from .modules.models import *
from .modules.db_queries import *
from sqlalchemy.orm import joinedload, validates
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict
from sqlalchemy import func
from datetime import datetime, date

event_manager_bp = Blueprint('event_manager', __name__, url_prefix='/evemng/<int:user_id>')

# Dashboard for event manager with the list of events
@event_manager_bp.route('/')
def event_manager(user_id):
    events = get_events(user_id)
    return render_template('event_manager/eventmanager_dash.html', events=events, user_id=user_id)

# View all events for a specific user
@event_manager_bp.route('/view_events')
def view_events(user_id):
    events = get_events(user_id)
    return render_template('event_manager/view_events.html', events=events, user_id=user_id)

@event_manager_bp.route('/event_details/<int:event_id>', methods=['GET'])
def event_details(user_id, event_id):
    try:
        # Check if the event_id corresponds to an Event or a SubEvent
        event = db.session.query(Event).filter_by(Event_ID=event_id, Event_Manager=user_id).first()

        if not event:  # If not found, check SubEvent
            sub_event = db.session.query(SubEvent).filter_by(Sub_Event_ID=event_id, Sub_Event_Manager=user_id).first()
            if not sub_event:
                flash("Event not found or you don't have permission to access it.", "danger")
                return redirect(url_for('event_manager.view_events', user_id=user_id))
            
            # If SubEvent is found, prepare its data
            event_data = {
                "id": sub_event.Sub_Event_ID,
                "event_name": sub_event.Name,
                "status": "Ongoing" if sub_event.Date == date.today() else "Completed" if sub_event.Date < date.today() else "Upcoming",
                "type": sub_event.event_type.Event_Type_Name,
                "department": sub_event.department.Name,
                "date": sub_event.Date,
                "time": sub_event.Time,
                "main_event_name": sub_event.event.Name  # Add the main event name for SubEvent
            }
            
            # Fetch transactions related to the sub-event
            transactions = db.session.query(Transaction).filter_by(Sub_Event_ID=sub_event.Sub_Event_ID).order_by(Transaction.Date.desc()).limit(5).all()
        
        else:
            # If Event is found, prepare its data
            event_data = {
                "id": event.Event_ID,
                "event_name": event.Name,
                "status": "Ongoing" if event.Date == date.today() else "Completed" if event.Date < date.today() else "Upcoming",
                "type": event.event_type.Event_Type_Name,
                "department": event.department.Name,
                "date": event.Date,
                "main_event_name": None  # No main event for regular Event
            }
            
            # Fetch transactions related to the event
            transactions = db.session.query(Transaction).filter_by(Event_ID=event.Event_ID).order_by(Transaction.Date.desc()).limit(5).all()

        # Prepare the transaction data for display
        transaction_data = []
        for transaction in transactions:
            # Get the transaction items and calculate the total amount
            transaction_items = db.session.query(TransactionItem).filter_by(Transaction_ID=transaction.Transaction_ID).all()
            total_amount = sum(item.Amount for item in transaction_items)
            
            # Append transaction details
            transaction_data.append({
                "bill_no": transaction.Bill_No,
                "party_name": transaction.Party_Name,
                "amount": total_amount,
                "date": transaction.Date
            })

        # Fetch event types for dropdowns in the form
        event_types = db.session.query(EventType).all()

        return render_template(
            'event_manager/event_details.html',
            event=event_data,
            event_types=event_types,
            user_id=user_id,
            is_sub_event=bool(not event),  # Boolean to indicate if it's a SubEvent
            transactions=transaction_data,  # Pass transactions to the template
        )

    except SQLAlchemyError as e:
        flash("An error occurred while fetching event details.", "danger")
        print(f"Error fetching event details: {e}")
        return redirect(url_for('event_manager.view_events', user_id=user_id))

# Update event or sub-event details
@event_manager_bp.route('/update_event/<int:event_id>', methods=['POST'])
def update_event(user_id, event_id):
    try:
        # Retrieve form data
        event_type = request.form.get('event_type')  # Event type (either 'event' or 'sub_event')
        date_str = request.form.get('date')  # Event date
        time_str = request.form.get('time')  # Time for SubEvent (optional)

        # Validate the necessary fields are present
        if not event_type or not date_str:
            flash("Required fields are missing.", "danger")
            return redirect(url_for('event_manager.event_details', user_id=user_id, event_id=event_id))

        # Process Event
        if event_type == 'event':
            filters = {'Event_ID': event_id, 'Event_Manager': user_id}
            updates = {'Date': date_str, 'Event_Type_ID': event_type}  # Using event_type directly in updates
            event = update_entry(Event, filters, updates)
            if event:
                flash("Event updated successfully!", "success")
            else:
                flash("Event not found or you don't have permission to edit it.", "danger")
                return redirect(url_for('event_manager.event_details', user_id=user_id, event_id=event_id))

        # Process SubEvent
        elif event_type == 'sub_event':
            filters = {'Sub_Event_ID': event_id, 'Sub_Event_Manager': user_id}
            updates = {'Date': date_str, 'Time': time_str, 'Event_Type_ID': event_type}  # Updating SubEvent
            sub_event = update_entry(SubEvent, filters, updates)
            if sub_event:
                flash("Sub-event updated successfully!", "success")
            else:
                flash("Sub-event not found or you don't have permission to edit it.", "danger")
                return redirect(url_for('event_manager.event_details', user_id=user_id, event_id=event_id))

        # If the event or sub-event is not found, show a message
        else:
            flash("Invalid event type.", "danger")

    except SQLAlchemyError as e:
        db.session.rollback()
        flash("An error occurred while updating the event.", "danger")
        print(f"Error updating event: {e}")
    
    return redirect(url_for('event_manager.event_details', user_id=user_id, event_id=event_id))


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

@event_manager_bp.route('/create_transaction/<int:event_id>', methods=['GET', 'POST'])
def create_transaction(user_id, event_id):
    try:
        if request.method == 'POST':
            # Fetch form data
            bill_no = request.form.get('bill_no')
            party_name = request.form.get('party_name')
            transaction_nature = request.form.get('transaction_nature')
            payment_mode = request.form.get('payment_mode')
            transaction_category = request.form.get('transaction_category')
            transaction_date = request.form.get('transaction_date')  # Fetch the selected date
            added_items = request.form.get('added_items')  # Get the dynamic items from hidden input

            # Validate the transaction date
            if not transaction_date:
                flash("Transaction date is required.", "danger")
                return redirect(url_for('event_manager.create_transaction', user_id=user_id, event_id=event_id))
            
            try:
                # Convert the date from the form to a Python date object
                transaction_date = datetime.strptime(transaction_date, "%Y-%m-%d").date()
            except ValueError:
                flash("Invalid date format. Please select a valid date.", "danger")
                return redirect(url_for('event_manager.create_transaction', user_id=user_id, event_id=event_id))

            # Ensure added_items is not empty
            if added_items:
                try:
                    # Parse the dynamic items (description and amount)
                    items = json.loads(added_items)  # Parsing the JSON string to a Python object
                except json.JSONDecodeError:
                    flash("Invalid item data format.", "danger")
                    return redirect(url_for('event_manager.create_transaction', user_id=user_id, event_id=event_id))
            else:
                flash("No items added to the transaction.", "danger")
                return redirect(url_for('event_manager.create_transaction', user_id=user_id, event_id=event_id))

            # Check if the event_id exists in the Event table
            event_exists = db.session.query(Event).filter_by(Event_ID=event_id).first()
            
            if event_exists:
                # If event exists, use the event_id as Event_ID
                transaction_data = {
                    'User_ID': user_id,
                    'Event_ID': event_id,  # Use the event_id directly as Event_ID
                    'Sub_Event_ID': None,
                    'Bill_No': bill_no,
                    'Party_Name': party_name,
                    'Nature_ID': transaction_nature,
                    'Mode_ID': payment_mode,
                    'Transaction_Category_ID': transaction_category,
                    'Date': transaction_date,  # Use the date from the form
                }
            else:
                # If event_id does not exist in the Event table, check the Sub_Event table
                sub_event_exists = db.session.query(SubEvent).filter_by(Sub_Event_ID=event_id).first()

                if not sub_event_exists:
                    flash("Event or Sub-Event not found.", "danger")
                    return redirect(url_for('event_manager.create_transaction', user_id=user_id, event_id=event_id))

                # If sub_event exists, retrieve the Event_ID from the SubEvent table
                transaction_data = {
                    'User_ID': user_id,
                    'Event_ID': sub_event_exists.Event_ID,  # Fetch Event_ID from the SubEvent table
                    'Sub_Event_ID': event_id,  # Use the provided event_id as Sub_Event_ID
                    'Bill_No': bill_no,
                    'Party_Name': party_name,
                    'Nature_ID': transaction_nature,
                    'Mode_ID': payment_mode,
                    'Transaction_Category_ID': transaction_category,
                    'Date': transaction_date,  # Use the date from the form
                }

            # Create the transaction entry in the database
            transaction_entry = create_entry(Transaction, **transaction_data)

            if transaction_entry:
                try:
                    # Add the items to the TransactionItem table
                    for item in items:
                        item_data = {
                            'Transaction_ID': transaction_entry.Transaction_ID,  # Reference the created transaction
                            'Description': item['description'],
                            'Amount': item['amount']
                        }
                        create_entry(TransactionItem, **item_data)  # Add each item to the TransactionItem table
                    
                    # Commit both transaction and items to the database
                    db.session.commit()
                    flash('Transaction and items created successfully.', 'success')

                except SQLAlchemyError as e:
                    # If an error happens while adding items, rollback changes
                    db.session.rollback()
                    flash("An error occurred while adding transaction items.", "danger")
                    print(f"Error adding items: {e}")

            else:
                flash('Failed to create transaction.', "danger")

            # Redirect to the event details page after successful creation
            return redirect(url_for('event_manager.event_details', event_id=event_id, user_id=user_id))

        # Fetch data for the form
        transaction_natures = db.session.query(TransactionNature).all()
        payment_modes = db.session.query(PaymentMode).all()
        transaction_categories = db.session.query(TransactionCategory).all()

        return render_template(
            'event_manager/create_transaction.html',
            event_id=event_id,
            transaction_natures=transaction_natures,
            payment_modes=payment_modes,
            transaction_categories=transaction_categories,
            user_id=user_id
        )

    except SQLAlchemyError as e:
        # Handle any errors
        flash("An error occurred while creating the transaction.", "danger")
        print(f"Error creating transaction: {e}")
        return redirect(url_for('event_manager.event_details', event_id=event_id, user_id=user_id))


@event_manager_bp.route('/event_transactions/<int:event_id>', methods=['GET'])
def view_all_transactions(user_id, event_id):
    try:
        # Fetch the Event or SubEvent based on the user ID
        event = db.session.query(Event).filter_by(Event_ID=event_id, Event_Manager=user_id).first()
        transactions = []

        if event:
            transactions = (
                db.session.query(Transaction)
                .filter_by(Event_ID=event_id)
                .order_by(Transaction.Date.desc())
                .all()
            )
        else:
            sub_event = db.session.query(SubEvent).filter_by(Sub_Event_ID=event_id, Sub_Event_Manager=user_id).first()

            if sub_event:
                parent_event_id = sub_event.Event_ID
                transactions = (
                    db.session.query(Transaction)
                    .filter(
                        (Transaction.Event_ID == parent_event_id) |
                        (Transaction.Sub_Event_ID == event_id)
                    )
                    .order_by(Transaction.Date.desc())
                    .all()
                )
            else:
                flash("Event or Sub-Event not found or you don't have permission to access it.", "danger")
                return redirect(url_for('event_manager.view_events', user_id=user_id))

        transaction_data = []
        for transaction in transactions:
            # Fetch related transaction items using the relationship defined in the model
            transaction_items = transaction.items  # Use the backref 'items' from the relationship

            # If no items are found, set the transaction_items to an empty list
            if not transaction_items:
                transaction_items = []

            total_amount = sum(item.Amount for item in transaction_items)

            # Create a dictionary for each transaction with its associated items
            transaction_data.append({
                "id":transaction.Transaction_ID,
                "bill_no": transaction.Bill_No,
                "party_name": transaction.Party_Name,
                "amount": total_amount,
                "date": transaction.Date,
                "nature": transaction.transaction_nature.Nature_Name,
                "payment_mode": transaction.payment_mode.Mode_Name,
                "category": transaction.transaction_category.Category_Name,
                "transaction_items": transaction_items  # Pass transaction items to template
            })

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        flash("An unexpected error occurred.", "danger")
    finally:
        # Ensure that the session is closed even if an error occurs
        db.session.close()
    print(transaction_data)
    return render_template(
        'event_manager/all_transactions.html',
        transactions=transaction_data,  # Pass processed transaction data
        event_id=event_id,
        user_id=user_id
    )


@event_manager_bp.route('/view_transaction/<int:transaction_id>', methods=['GET'])
def view_individual_transaction(user_id,transaction_id):
    try:
        # Fetch the transaction details
        transaction = Transaction.query.get_or_404(transaction_id)

        # Fetch the associated transaction items, ensuring you're executing the query
        items = TransactionItem.query.filter_by(Transaction_ID=transaction_id).all()  # Use .all() to get a list

        # Prepare data for rendering
        transaction_data = transaction.to_dict()
        item_data = [{'TransactionItem_ID': item.TransactionItem_ID, 'Description': item.Description, 'Amount': item.Amount} for item in items]

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return render_template("error.html", message="An error occurred while fetching the transaction."), 500

    return render_template("event_manager/view_transaction.html", transaction=transaction_data, user_id=user_id, items=item_data)


@event_manager_bp.route('/delete_transaction_item/<int:item_id>', methods=['GET'])
def delete_transaction_item(user_id, item_id):
    item = TransactionItem.query.get_or_404(item_id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Transaction item deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting item: {e}', 'danger')
    return redirect(request.referrer)


@event_manager_bp.route('/edit_transaction_item/<int:item_id>', methods=['POST'])
def edit_transaction_item(user_id, item_id):
    item = TransactionItem.query.get_or_404(item_id)
    description = request.form['description']
    amount = request.form['amount']
    
    try:
        item.Description = description
        item.Amount = amount
        db.session.commit()
        flash('Transaction item updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating item: {e}', 'danger')
    
    return redirect(request.referrer)
