# Notification Triggers Quick Reference

## Event Manager Notifications

### Receives notifications when:
1. ✅ **Event Assignment** (from Admin)
   - Assigned as event manager to new single event
   - Assigned as main event manager to multi-day event

2. ✅ **Event Reassignment** (from Admin)
   - Added as event manager to existing event
   - Removed from event management role

3. ✅ **Report Generated** (from Finance Manager)
   - Excel report downloaded for their event
   - PDF report downloaded for their event

## Finance Manager Notifications

### Receives notifications when:
1. ✅ **Event Assignment** (from Admin)
   - Assigned as finance manager to new single event
   - Assigned as main finance manager to multi-day event

2. ✅ **Event Reassignment** (from Admin)
   - Added as finance manager to existing event
   - Removed from finance management role

3. ✅ **Transaction Created** (from Event Manager)
   - New transaction added to any of their events
   - Includes transaction type and amount

4. ✅ **Large Transaction** (from Event Manager)
   - Transaction ≥ ₹10,000 created
   - Warning-level notification

5. ✅ **Transaction Updated** (from Event Manager)
   - Existing transaction modified
   - Includes new total amount

6. ✅ **Budget Thresholds** (Automatic)
   - 50% of budget used (info)
   - 75% of budget used (warning)
   - 90% of budget used (danger)
   - 100% budget exceeded (danger)

## Sub-Event Manager Notifications

### Receives notifications when:
1. ✅ **Sub-Event Assignment** (from Admin)
   - Assigned to manage a specific sub-event
   - Includes sub-event name and date

## All Users

### Receive notifications when:
1. ✅ **Account Created** (from Admin)
   - Welcome message with default credentials

2. ✅ **Role Changed** (from Admin)
   - Role update notification
   - Requires re-authorization

3. ✅ **Profile Updates** (Self)
   - Password changed successfully
   - Profile updated successfully

## Notification Types

| Type | Color | Use Case | Examples |
|------|-------|----------|----------|
| **info** | Blue | General information | Transaction created, Report generated |
| **success** | Green | Positive actions | Event assignment, Account created |
| **warning** | Yellow | Important changes | Transaction updated, Role changed, Manager removed |
| **danger** | Red | Critical alerts | Budget exceeded, Budget at 90% |

## Budget Alert Thresholds

| Threshold | Type | Icon | Triggered When |
|-----------|------|------|----------------|
| 50% | info | 📊 | Half budget spent |
| 75% | warning | ⚠️ | Three-quarters budget spent |
| 90% | danger | 🚨 | Nearly all budget spent |
| 100% | danger | ⚠️ | Budget exceeded |

## Large Transaction Alert

- **Threshold**: ₹10,000
- **Type**: warning
- **Icon**: 💰
- **Recipients**: Finance Manager + Event Manager (if different from creator)
- **Triggered**: When any transaction ≥ ₹10,000 is created

## Activity Log Entries

All the following actions are logged in Activity Log (Admin view):

### User Actions
- User created
- User updated
- User role changed

### Event Actions
- Event created (single/multiple)
- Event updated
- Manager assigned/removed

### Transaction Actions
- Transaction created
- Transaction updated

### Report Actions
- Excel report generated
- PDF report generated

Each log entry includes:
- User who performed action
- Action type (created/updated/deleted)
- Entity type and ID
- Description
- Timestamp
- IP Address
- User Agent

## Notification Access

### View Notifications
- **Event Manager**: `/event_manager/<user_id>/notifications`
- **Finance Manager**: `/finance_manager/<user_id>/notifications`
- **Admin**: `/admin/notifications`

### Mark as Read
- **Single**: Click notification or use "Mark as Read" button
- **All**: Click "Mark all as read" button

### Activity Log (Admin Only)
- **Access**: `/admin/activity-log`
- **Shows**: All system activities in chronological order
