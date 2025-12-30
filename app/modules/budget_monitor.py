"""
Budget Monitoring Utility
Checks budget thresholds and creates notifications
"""
from app import db
from .models import Event, Budget, Transaction, TransactionItem
from .activity_logger import create_notification


def check_budget_thresholds(event_id):
    """
    Check budget usage and send notifications if thresholds are crossed
    
    Args:
        event_id: ID of the event to check
    
    Returns:
        dict: Budget status information
    """
    try:
        event = Event.query.get(event_id)
        if not event:
            return None
        
        # Get budget
        budget = Budget.query.filter_by(Event_ID=event_id).first()
        if not budget:
            return None
        
        budget_amount = float(budget.Amount)
        
        # Calculate total expenses
        transactions = Transaction.query.filter_by(Event_ID=event_id).all()
        total_expense = 0
        
        for txn in transactions:
            if txn.transaction_nature and txn.transaction_nature.Nature_Name == 'Expense':
                for item in txn.items:
                    total_expense += float(item.Amount)
        
        # Calculate usage percentage
        usage_percentage = (total_expense / budget_amount * 100) if budget_amount > 0 else 0
        remaining = budget_amount - total_expense
        
        # Determine notification type and message
        notification_data = None
        
        if usage_percentage >= 100:
            notification_data = {
                'title': '⚠️ Budget Exceeded!',
                'message': f'Event "{event.Name}" has exceeded its budget! Spent: ₹{total_expense:,.2f} / Budget: ₹{budget_amount:,.2f} ({usage_percentage:.1f}%)',
                'type': 'danger'
            }
        elif usage_percentage >= 90:
            notification_data = {
                'title': '🚨 Budget Alert - 90% Used',
                'message': f'Event "{event.Name}" has used 90% of its budget. Spent: ₹{total_expense:,.2f} / Budget: ₹{budget_amount:,.2f}. Remaining: ₹{remaining:,.2f}',
                'type': 'danger'
            }
        elif usage_percentage >= 75:
            notification_data = {
                'title': '⚠️ Budget Warning - 75% Used',
                'message': f'Event "{event.Name}" has used 75% of its budget. Spent: ₹{total_expense:,.2f} / Budget: ₹{budget_amount:,.2f}. Remaining: ₹{remaining:,.2f}',
                'type': 'warning'
            }
        elif usage_percentage >= 50:
            notification_data = {
                'title': '📊 Budget Milestone - 50% Used',
                'message': f'Event "{event.Name}" has used half of its budget. Spent: ₹{total_expense:,.2f} / Budget: ₹{budget_amount:,.2f}. Remaining: ₹{remaining:,.2f}',
                'type': 'info'
            }
        
        # Send notifications if threshold crossed
        if notification_data:
            # Notify Event Manager
            if event.Event_Manager:
                create_notification(
                    user_id=event.Event_Manager,
                    title=notification_data['title'],
                    message=notification_data['message'],
                    notification_type=notification_data['type'],
                    event_id=event_id
                )
            
            # Notify Finance Manager
            if event.Finance_Manager:
                create_notification(
                    user_id=event.Finance_Manager,
                    title=notification_data['title'],
                    message=notification_data['message'],
                    notification_type=notification_data['type'],
                    event_id=event_id
                )
        
        return {
            'budget': budget_amount,
            'spent': total_expense,
            'remaining': remaining,
            'usage_percentage': usage_percentage,
            'status': 'exceeded' if usage_percentage >= 100 else 'warning' if usage_percentage >= 75 else 'normal'
        }
    
    except Exception as e:
        print(f"Error checking budget thresholds: {e}")
        return None


def notify_large_transaction(user_id, transaction_id, amount, event_id, threshold=10000):
    """
    Notify relevant parties about large transactions
    
    Args:
        user_id: User who created the transaction
        transaction_id: ID of the transaction
        amount: Transaction amount
        event_id: Related event ID
        threshold: Amount threshold (default: 10000)
    """
    try:
        if amount >= threshold:
            event = Event.query.get(event_id)
            if not event:
                return
            
            message = f'Large transaction of ₹{amount:,.2f} was created in event "{event.Name}"'
            
            # Notify Finance Manager
            if event.Finance_Manager and event.Finance_Manager != user_id:
                create_notification(
                    user_id=event.Finance_Manager,
                    title='💰 Large Transaction Alert',
                    message=message,
                    notification_type='warning',
                    event_id=event_id,
                    transaction_id=transaction_id
                )
            
            # Notify Event Manager if different from creator
            if event.Event_Manager and event.Event_Manager != user_id:
                create_notification(
                    user_id=event.Event_Manager,
                    title='💰 Large Transaction Alert',
                    message=message,
                    notification_type='warning',
                    event_id=event_id,
                    transaction_id=transaction_id
                )
    
    except Exception as e:
        print(f"Error notifying large transaction: {e}")
