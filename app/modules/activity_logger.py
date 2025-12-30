"""
Activity Logger Module
Handles logging user activities and creating notifications
"""
from app import db
from .models import ActivityLog, Notification
from flask import request
from datetime import datetime


def log_activity(user_id, action, entity_type, entity_id, description):
    """
    Log a user activity
    
    Args:
        user_id: ID of the user performing the action
        action: Type of action (created, updated, deleted, etc.)
        entity_type: Type of entity affected (Event, Transaction, User, etc.)
        entity_id: ID of the affected entity
        description: Human-readable description of the action
    """
    try:
        # Get IP address from request
        ip_address = request.remote_addr if request else None
        
        activity = ActivityLog(
            User_ID=user_id,
            Action=action,
            Entity_Type=entity_type,
            Entity_ID=entity_id,
            Description=description,
            IP_Address=ip_address,
            Timestamp=datetime.now()
        )
        
        db.session.add(activity)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error logging activity: {e}")
        db.session.rollback()
        return False


def create_notification(user_id, title, message, notification_type='info', event_id=None, transaction_id=None):
    """
    Create a notification for a user
    
    Args:
        user_id: ID of the user to notify
        title: Notification title
        message: Notification message
        notification_type: Type of notification (info, success, warning, danger)
        event_id: Optional related event ID
        transaction_id: Optional related transaction ID
    """
    try:
        notification = Notification(
            User_ID=user_id,
            Title=title,
            Message=message,
            Type=notification_type,
            Is_Read=False,
            Created_At=datetime.now(),
            Related_Event_ID=event_id,
            Related_Transaction_ID=transaction_id
        )
        
        db.session.add(notification)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error creating notification: {e}")
        db.session.rollback()
        return False


def get_unread_notification_count(user_id):
    """Get count of unread notifications for a user"""
    try:
        return Notification.query.filter_by(User_ID=user_id, Is_Read=False).count()
    except Exception as e:
        print(f"Error getting notification count: {e}")
        return 0


def mark_notification_read(notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.query.get(notification_id)
        if notification:
            notification.Is_Read = True
            db.session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error marking notification as read: {e}")
        db.session.rollback()
        return False


def mark_all_notifications_read(user_id):
    """Mark all notifications as read for a user"""
    try:
        Notification.query.filter_by(User_ID=user_id, Is_Read=False).update({'Is_Read': True})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error marking all notifications as read: {e}")
        db.session.rollback()
        return False
