from app import db
from .models import *
from .db_queries import filter_data
from sqlalchemy.exc import SQLAlchemyError

def get_transaction_ids(event_id, transaction_nature=None, transaction_category=None, transaction_mode=None):
    """Fetch Transaction_IDs from the Transaction table based on the provided filters."""
    filters = {"Event_ID": event_id}
    
    # Add filters only if the filter value is not None
    if transaction_nature is not None:
        filters["Nature_ID"] = transaction_nature
    if transaction_category is not None:
        filters["Transaction_Category_ID"] = transaction_category
    if transaction_mode is not None:
        filters["Mode_ID"] = transaction_mode

    transactions = filter_data(Transaction, filters=filters, columns=["Transaction_ID"])
    
    transaction_ids = []
    for transaction in transactions:
        transaction_ids.append(transaction.Transaction_ID)  # Collecting each Transaction_ID one by one
    return transaction_ids


def get_transaction_ids_by_nature(event_id, nature_id, is_sub_event=False):
    """Fetch Transaction_IDs based on Transaction-Nature for a specific event or sub-event."""
    filters = {"Nature_ID": nature_id}
    if is_sub_event:
        filters["Sub_Event_ID"] = event_id
    else:
        filters["Event_ID"] = event_id

    transactions = filter_data(Transaction, filters=filters, columns=["Transaction_ID"])
    
    transaction_ids = []
    for transaction in transactions:
        transaction_ids.append(transaction.Transaction_ID)  # Collecting each Transaction_ID one by one
    return transaction_ids


def get_transaction_ids_by_category(event_id, category_id, is_sub_event=False):
    """Fetch Transaction_IDs based on Transaction-Category for a specific event or sub-event."""
    filters = {"Transaction_Category_ID": category_id}
    if is_sub_event:
        filters["Sub_Event_ID"] = event_id
    else:
        filters["Event_ID"] = event_id

    transactions = filter_data(Transaction, filters=filters, columns=["Transaction_ID"])
    
    transaction_ids = []
    for transaction in transactions:
        transaction_ids.append(transaction.Transaction_ID)  # Collecting each Transaction_ID one by one
    return transaction_ids


def get_transaction_ids_by_mode(event_id, mode_id, is_sub_event=False):
    """Fetch Transaction_IDs based on Transaction-Mode for a specific event or sub-event."""
    filters = {"Mode_ID": mode_id}
    if is_sub_event:
        filters["Sub_Event_ID"] = event_id
    else:
        filters["Event_ID"] = event_id

    transactions = filter_data(Transaction, filters=filters, columns=["Transaction_ID"])
    
    transaction_ids = []
    for transaction in transactions:
        transaction_ids.append(transaction.Transaction_ID)  # Collecting each Transaction_ID one by one
    return transaction_ids


def get_transaction_amounts(transaction_ids):
    """Fetch amounts from TransactionItem table for the given list of Transaction_IDs."""
    if not transaction_ids:
        return []  # Return an empty list if no IDs are provided

    try:
        amounts = []
        for transaction_id in transaction_ids:
            # Query for each transaction ID individually
            transaction_items = filter_data(TransactionItem, filters={"Transaction_ID": transaction_id}, columns=["Amount"])
            
            for item in transaction_items:
                amounts.append(item.Amount)  # Collecting each Amount one by one
        return amounts
    except SQLAlchemyError as e:
        print(f"Error reading entries: {e}")
        return []



def calculate_total_amount(transaction_ids):
    """Calculate the total amount for the given list of Transaction_IDs."""
    amounts = get_transaction_amounts(transaction_ids)
    total = sum(amounts)
    return total


def get_revenue_total(event_id, is_sub_event=False):
    """
    Get total revenue amount for a specific event or sub-event.
    Revenue corresponds to a specific Transaction-Nature (e.g., 'Revenue').
    """
    nature_id = get_nature_id("Revenue")  # Dynamically fetch Nature_ID
    if not nature_id:
        raise ValueError("Revenue nature not found.")
    transaction_ids = get_transaction_ids_by_nature(event_id, nature_id, is_sub_event)
    return calculate_total_amount(transaction_ids)

def get_expense_total(event_id, is_sub_event=False):
    """
    Get total expense amount for a specific event or sub-event.
    Expense corresponds to a specific Transaction-Nature (e.g., 'Expense').
    """
    nature_id = get_nature_id("Expense")  # Dynamically fetch Nature_ID
    if not nature_id:
        raise ValueError("Expense nature not found.")
    transaction_ids = get_transaction_ids_by_nature(event_id, nature_id, is_sub_event)
    return calculate_total_amount(transaction_ids)

def get_category_total(event_id, category_id, is_sub_event=False):
    """
    Get total amount for a specific Transaction-Category in an event or sub-event.
    """
    transaction_ids = get_transaction_ids_by_category(event_id, category_id, is_sub_event)
    return calculate_total_amount(transaction_ids)

def get_mode_total(event_id, mode_id, is_sub_event=False):
    """
    Get total amount for a specific Transaction-Mode in an event or sub-event.
    """
    transaction_ids = get_transaction_ids_by_mode(event_id, mode_id, is_sub_event)
    return calculate_total_amount(transaction_ids)

def get_nature_id(nature_name):
    """
    Fetch Nature_ID based on Nature_Name (e.g., 'Revenue', 'Expense').
    """
    nature = filter_data(TransactionNature, filters={"Nature_Name": nature_name}, columns=["Nature_ID"])
    return nature[0].Nature_ID if nature else None

# Helper Function: Fetch All Transaction Category IDs
def get_all_transaction_category_ids():
    try:
        categories = db.session.query(TransactionCategory.Transaction_Category_ID).all()
        return [category[0] for category in categories]
    except SQLAlchemyError as e:
        print("Error fetching transaction categories:", e)
        return []

# Helper Function: Fetch All Payment Mode IDs
def get_all_payment_mode_ids():
    try:
        modes = db.session.query(PaymentMode.Mode_ID).all()
        return [mode[0] for mode in modes]
    except SQLAlchemyError as e:
        print("Error fetching payment modes:", e)
        return []


def get_category_name(category_id):
    """Fetch Category Name based on Transaction Category ID."""
    category = filter_data(TransactionCategory, filters={"Transaction_Category_ID": category_id}, columns=["Category_Name"])
    return category[0].Category_Name if category else "Unknown Category"

def get_mode_name(mode_id):
    """Fetch Payment Mode Name based on Mode ID."""
    mode = filter_data(PaymentMode, filters={"Mode_ID": mode_id}, columns=["Mode_Name"])
    return mode[0].Mode_Name if mode else "Unknown Mode"


