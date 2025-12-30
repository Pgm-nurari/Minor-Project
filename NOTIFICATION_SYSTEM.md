# FinSight Notification System Documentation

## Overview
The FinSight application includes a comprehensive notification and activity logging system that keeps all users informed about important events, changes, and actions within the system.

## Features

### 1. Real-time Notifications
- **Visual Indicators**: Notification bell icon in header with unread count badge
- **Notification Types**: 
  - `info` (blue) - Informational messages
  - `success` (green) - Positive actions like assignments
  - `warning` (yellow) - Important changes or alerts
  - `danger` (red) - Critical alerts and budget overruns

### 2. Activity Logging
- Complete audit trail of all system actions
- Tracks user, action type, timestamp, IP address
- Filterable timeline view for admins

### 3. Budget Monitoring
- Automatic budget threshold notifications
- Alerts at 50%, 75%, 90%, and 100% of budget
- Large transaction warnings (₹10,000+)

## Notification Triggers

### Admin Operations

#### Event Creation
**Single Event:**
- **Triggers**: When admin creates a new event
- **Recipients**: 
  - Event Manager (success notification)
  - Finance Manager (success notification)
- **Message**: "You have been assigned as [Event/Finance] Manager for event '[Event Name]'"

**Multi-Day Events:**
- **Triggers**: When admin creates event with sub-events
- **Recipients**:
  - Main Event Manager (success)
  - Main Finance Manager (success)
  - Each Sub-Event Manager (individual success notifications)
- **Message**: Includes specific event/sub-event details and dates

#### Event Updates
**Manager Reassignment:**
- **Triggers**: When admin changes event/finance manager
- **Recipients**:
  - Old managers (warning - removed notification)
  - New managers (success - assignment notification)
- **Messages**: 
  - Removed: "You have been removed as [Role] from event '[Event Name]'"
  - Assigned: "You have been assigned as [Role] for event '[Event Name]'"

#### User Management
**New User Creation:**
- **Triggers**: When admin creates new user
- **Recipients**: The new user
- **Type**: info
- **Message**: Welcome message with default credentials

**Role Change:**
- **Triggers**: When admin changes user role
- **Recipients**: The affected user
- **Type**: warning
- **Message**: "Your role has been changed from [Old Role] to [New Role]. Please contact admin for re-authorization."

### Event Manager Operations

#### Transaction Creation
**Standard Transaction:**
- **Triggers**: When event manager creates transaction
- **Recipients**: Finance Manager of the event
- **Type**: info
- **Message**: "Event Manager created a new [Nature] transaction for ₹[Amount] in event '[Event Name]'"

**Large Transaction (₹10,000+):**
- **Triggers**: Transaction amount >= ₹10,000
- **Recipients**: 
  - Finance Manager (warning)
  - Event Manager (if different from creator)
- **Type**: warning
- **Message**: "Large transaction of ₹[Amount] was created in event '[Event Name]'"

**Budget Threshold Crossed:**
- **Triggers**: After transaction creation/update if budget threshold crossed
- **Recipients**: Both Event Manager and Finance Manager
- **Types**: 
  - 50%: info
  - 75%: warning
  - 90%: danger
  - 100%: danger (Budget Exceeded!)
- **Messages**: Include spent amount, budget amount, and remaining amount

#### Transaction Updates
- **Triggers**: When event manager edits transaction
- **Recipients**: Finance Manager
- **Type**: warning
- **Message**: "Event Manager updated transaction [Bill No] - New total: ₹[Amount] in event '[Event Name]'"

### Finance Manager Operations

#### Report Generation
**Excel Report:**
- **Triggers**: When finance manager downloads Excel report
- **Recipients**: Event Manager of the event
- **Type**: info
- **Message**: "Finance Manager generated Excel report for event '[Event Name]'"

**PDF Report:**
- **Triggers**: When finance manager downloads PDF report
- **Recipients**: Event Manager of the event
- **Type**: info
- **Message**: "Finance Manager generated PDF report for event '[Event Name]'"

## Budget Monitoring System

### Automatic Checks
The budget monitoring system automatically checks budget usage:
- After every transaction creation
- After every transaction update
- Calculates total expenses vs. budget in real-time

### Threshold Alerts

#### 50% Budget Used
- **Type**: info (📊)
- **Title**: "Budget Milestone - 50% Used"
- **Recipients**: Event Manager & Finance Manager

#### 75% Budget Used
- **Type**: warning (⚠️)
- **Title**: "Budget Warning - 75% Used"
- **Recipients**: Event Manager & Finance Manager

#### 90% Budget Used
- **Type**: danger (🚨)
- **Title**: "Budget Alert - 90% Used"
- **Recipients**: Event Manager & Finance Manager

#### 100% Budget Exceeded
- **Type**: danger (⚠️)
- **Title**: "Budget Exceeded!"
- **Recipients**: Event Manager & Finance Manager
- **Message**: Includes overspending details

### Large Transaction Alerts
- **Threshold**: ₹10,000
- **Type**: warning (💰)
- **Title**: "Large Transaction Alert"
- **Recipients**: Finance Manager & Event Manager (if different)

## Activity Logging

### Tracked Actions
All the following actions are logged:
1. **User Management**
   - User creation
   - User updates
   - Role changes

2. **Event Management**
   - Event creation (single & multiple)
   - Event updates
   - Manager assignments/removals

3. **Transaction Management**
   - Transaction creation
   - Transaction updates

4. **Report Generation**
   - Excel report downloads
   - PDF report downloads

### Log Information
Each log entry includes:
- User who performed the action
- Action type (created/updated/deleted)
- Entity type (User/Event/Transaction)
- Entity ID
- Descriptive message
- Timestamp
- IP Address
- User Agent

## User Interface

### Notification Bell
- **Location**: Top-right corner of all headers
- **Badge**: Shows unread notification count
- **Dropdown**: Quick view of recent notifications
- **Actions**:
  - Click notification to mark as read
  - "Mark all as read" button
  - "View all notifications" link

### Notification Page
- **Access**: Click "View all" in dropdown or navigate from menu
- **Features**:
  - Paginated list of all notifications
  - Color-coded by type
  - Timestamps (relative and absolute)
  - Mark individual notifications as read
  - Filter by type (future enhancement)

### Activity Log (Admin Only)
- **Access**: Admin dashboard sidebar
- **Display**: Timeline view
- **Color Coding**:
  - Green: created
  - Blue: updated
  - Red: deleted
- **Information**: User, action, entity, description, timestamp, IP

## Database Schema

### Notification Table
```sql
CREATE TABLE Notification (
    Notification_ID INT PRIMARY KEY AUTO_INCREMENT,
    User_ID INT NOT NULL,
    Title VARCHAR(255) NOT NULL,
    Message TEXT NOT NULL,
    Type ENUM('info', 'success', 'warning', 'danger') DEFAULT 'info',
    Is_Read BOOLEAN DEFAULT FALSE,
    Related_Event_ID INT,
    Related_Transaction_ID INT,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Related_Event_ID) REFERENCES Event(Event_ID),
    FOREIGN KEY (Related_Transaction_ID) REFERENCES transaction_table(Transaction_ID)
);
```

### Activity_Log Table
```sql
CREATE TABLE Activity_Log (
    Log_ID INT PRIMARY KEY AUTO_INCREMENT,
    User_ID INT NOT NULL,
    Action VARCHAR(50) NOT NULL,
    Entity_Type VARCHAR(50),
    Entity_ID INT,
    Description TEXT,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IP_Address VARCHAR(45),
    User_Agent TEXT,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);
```

## Helper Functions

### activity_logger.py

#### create_notification()
```python
create_notification(
    user_id,           # Required: Recipient user ID
    title,             # Required: Notification title
    message,           # Required: Notification message
    notification_type, # Optional: info/success/warning/danger
    event_id,          # Optional: Related event ID
    transaction_id     # Optional: Related transaction ID
)
```

#### log_activity()
```python
log_activity(
    user_id,        # Required: User performing action
    action,         # Required: created/updated/deleted
    entity_type,    # Optional: User/Event/Transaction
    entity_id,      # Optional: ID of affected entity
    description     # Optional: Human-readable description
)
```

#### get_unread_notification_count()
```python
count = get_unread_notification_count(user_id)
```

#### mark_notification_read()
```python
mark_notification_read(notification_id)
```

#### mark_all_notifications_read()
```python
mark_all_notifications_read(user_id)
```

### budget_monitor.py

#### check_budget_thresholds()
```python
status = check_budget_thresholds(event_id)
# Returns: {
#     'budget': float,
#     'spent': float,
#     'remaining': float,
#     'usage_percentage': float,
#     'status': 'exceeded'|'warning'|'normal'
# }
```

#### notify_large_transaction()
```python
notify_large_transaction(
    user_id,         # User who created transaction
    transaction_id,  # Transaction ID
    amount,          # Transaction amount
    event_id,        # Related event ID
    threshold=10000  # Optional: Custom threshold
)
```

## Testing

### Manual Testing Checklist
1. ✅ Create new user - Check welcome notification
2. ✅ Create event - Check manager notifications
3. ✅ Create multi-day event - Check all manager notifications
4. ✅ Edit event managers - Check old/new manager notifications
5. ✅ Create transaction - Check finance manager notification
6. ✅ Create large transaction - Check warning notifications
7. ✅ Edit transaction - Check update notification
8. ✅ Cross budget threshold - Check budget alerts
9. ✅ Generate Excel report - Check event manager notification
10. ✅ Generate PDF report - Check event manager notification
11. ✅ Change user role - Check role change notification
12. ✅ View activity log - Check all logged actions

### Automated Tests
See `test_notifications.py` for automated test suite.

## Future Enhancements

### Planned Features
1. **Email Notifications**: Send email copies of important notifications
2. **Event Date Reminders**: 
   - 7 days before event
   - 3 days before event
   - 1 day before event
   - Overdue event alerts
3. **Notification Preferences**: Allow users to customize notification types
4. **Mobile Push Notifications**: For mobile app integration
5. **Notification Scheduling**: Schedule notifications for future delivery
6. **Notification Categories**: Group notifications by category
7. **Search and Filter**: Search notifications by keyword, filter by type/date
8. **Export Activity Logs**: Export logs to CSV/Excel for audit purposes

### Performance Optimizations
1. **Pagination**: Already implemented for notification list
2. **Archive Old Notifications**: Move old read notifications to archive table
3. **Notification Batching**: Combine similar notifications into digest
4. **Real-time Updates**: WebSocket integration for instant notifications
5. **Caching**: Cache unread counts to reduce database queries

## Configuration

### Notification Settings
Located in `app/config.py` (can be added):
```python
NOTIFICATION_SETTINGS = {
    'LARGE_TRANSACTION_THRESHOLD': 10000,
    'BUDGET_THRESHOLDS': [50, 75, 90, 100],
    'ENABLE_EMAIL_NOTIFICATIONS': False,
    'NOTIFICATIONS_PER_PAGE': 20,
    'AUTO_ARCHIVE_DAYS': 90
}
```

## Troubleshooting

### Common Issues

**Notifications not appearing:**
1. Check database connection
2. Verify user_id is correct
3. Check notification table for entries
4. Verify notification bell JavaScript is loaded

**Budget alerts not triggering:**
1. Ensure transaction has items with amounts
2. Check if budget exists for event
3. Verify transaction nature is set correctly
4. Check budget_monitor.py is being called

**Activity log not recording:**
1. Verify log_activity() is called after actions
2. Check Activity_Log table exists
3. Verify user session is active
4. Check for database write permissions

## Support
For issues or questions, contact the development team or check the GitHub repository for updates.
