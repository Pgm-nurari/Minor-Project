from app import db
from sqlalchemy import CheckConstraint, func, DECIMAL
from sqlalchemy.orm import validates

class BaseMixin:
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Department(db.Model, BaseMixin):
    __tablename__ = 'Department'
    Dept_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)

class Role(db.Model, BaseMixin):
    __tablename__ = 'Role'
    Role_ID = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(50), nullable=False)

class User(db.Model, BaseMixin):
    __tablename__ = 'User'
    User_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False, default="")  # Default empty password
    Role = db.Column(db.Integer, db.ForeignKey('Role.Role_ID'))
    Dept_ID = db.Column(db.Integer, db.ForeignKey('Department.Dept_ID'))  # Foreign key reference to Department
    Verified = db.Column(db.Integer, default=0, nullable=False)  # Default value of 0, only 0 or 1 are valid
    modified_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    department = db.relationship('Department', backref='users', lazy=True)
    role = db.relationship('Role', backref='users', lazy=True)

class EventType(db.Model, BaseMixin):
    __tablename__ = 'Event_Type'
    Event_Type_ID = db.Column(db.Integer, primary_key=True)
    Event_Type_Name = db.Column(db.String(50), nullable=False)

class Event(db.Model, BaseMixin):
    __tablename__ = 'Event'
    Event_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Finance_Manager = db.Column(db.Integer, db.ForeignKey('User.User_ID'))  # Renamed User_ID to Finance_Manager
    Event_Manager = db.Column(db.Integer, db.ForeignKey('User.User_ID'))  # Added new Event_Manager column
    Name = db.Column(db.String(100), nullable=False)
    Event_Type_ID = db.Column(db.Integer, db.ForeignKey('Event_Type.Event_Type_ID'))
    Date = db.Column(db.Date, nullable=False)
    Days = db.Column(db.Integer, nullable=False)
    Dept_ID = db.Column(db.Integer, db.ForeignKey('Department.Dept_ID'))  # Foreign key to Department
    modified_date = db.Column(db.DateTime, default=func.current_timestamp())

    # Relationships to the User, EventType, and Department models
    finance_manager = db.relationship('User', foreign_keys=[Finance_Manager], backref='finance_managed_events', lazy=True)
    event_manager = db.relationship('User', foreign_keys=[Event_Manager], backref='managed_events', lazy=True)
    event_type = db.relationship('EventType', backref='events', lazy=True)
    department = db.relationship('Department', backref='events', lazy=True)

class SubEvent(db.Model, BaseMixin):
    __tablename__ = 'Sub_Event'
    Sub_Event_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Sub_Event_Manager = db.Column(db.Integer, db.ForeignKey('User.User_ID'))  # Renamed User_ID to Sub_Event_Manager
    Name = db.Column(db.String(100), nullable=False)
    Event_Type_ID = db.Column(db.Integer, db.ForeignKey('Event_Type.Event_Type_ID'))
    Date = db.Column(db.Date, nullable=False)
    Time = db.Column(db.Time, nullable=False)
    Dept_ID = db.Column(db.Integer, db.ForeignKey('Department.Dept_ID'))  # Foreign key to Department
    Event_ID = db.Column(db.Integer, db.ForeignKey('Event.Event_ID'))
    modified_date = db.Column(db.DateTime, default=func.current_timestamp())

    # Relationships to User, EventType, Department, and Event models
    sub_event_manager = db.relationship('User', foreign_keys=[Sub_Event_Manager], backref='sub_events_managed', lazy=True)
    event_type = db.relationship('EventType', backref='sub_events', lazy=True)
    department = db.relationship('Department', backref='sub_events', lazy=True)
    event = db.relationship('Event', backref='sub_events', lazy=True)

class AccountCategory(db.Model, BaseMixin):
    __tablename__ = 'Account_Category'
    Account_Category_ID = db.Column(db.Integer, primary_key=True)
    Category_Name = db.Column(db.String(50), nullable=False, unique=True)


class TransactionCategory(db.Model, BaseMixin):
    __tablename__ = 'Transaction_Category'
    Transaction_Category_ID = db.Column(db.Integer, primary_key=True)
    Category_Name = db.Column(db.String(50), nullable=False, unique=True)


class PaymentMode(db.Model, BaseMixin):
    __tablename__ = 'Payment_Mode'
    Mode_ID = db.Column(db.Integer, primary_key=True)
    Mode_Name = db.Column(db.String(50), nullable=False, unique=True)


class TransactionNature(db.Model, BaseMixin):
    __tablename__ = 'Transaction_Nature'
    Nature_ID = db.Column(db.Integer, primary_key=True)
    Nature_Name = db.Column(db.String(50), nullable=False, unique=True)


class Transaction(db.Model, BaseMixin):
    __tablename__ = 'transaction_table'
    Transaction_ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('User.User_ID'), nullable=False)
    Event_ID = db.Column(db.Integer, db.ForeignKey('Event.Event_ID'), nullable=False)
    Sub_Event_ID = db.Column(db.Integer, db.ForeignKey('Sub_Event.Sub_Event_ID'), nullable=True)  # New column for SubEvent
    Amount = db.Column(DECIMAL(10, 2), default=0.00)
    Bill_No = db.Column(db.String(50), nullable=True)
    Party_Name = db.Column(db.String(100), nullable=True)
    Nature_ID = db.Column(db.Integer, db.ForeignKey('Transaction_Nature.Nature_ID'))
    Mode_ID = db.Column(db.Integer, db.ForeignKey('Payment_Mode.Mode_ID'))
    Date = db.Column(db.Date, nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Transaction_Category_ID = db.Column(db.Integer, db.ForeignKey('Transaction_Category.Transaction_Category_ID'))
    Account_Category_ID = db.Column(db.Integer, db.ForeignKey('Account_Category.Account_Category_ID'))
    modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships with foreign key models
    user = db.relationship('User', backref='transactions', lazy=True)
    event = db.relationship('Event', backref='transactions', lazy=True)
    sub_event = db.relationship('SubEvent', backref='transactions', lazy=True)  # New relationship for SubEvent
    transaction_nature = db.relationship('TransactionNature', backref='transactions', lazy=True)
    payment_mode = db.relationship('PaymentMode', backref='transactions', lazy=True)
    transaction_category = db.relationship('TransactionCategory', backref='transactions', lazy=True)
    account_category = db.relationship('AccountCategory', backref='transactions', lazy=True)

        
class TransactionItem(db.Model):
    __tablename__ = 'transactionitem'

    # Make sure these are the correct column names
    TransactionItem_ID = db.Column(db.Integer, primary_key=True)
    Transaction_ID = db.Column(db.Integer, db.ForeignKey('transaction_table.Transaction_ID'))
    Description = db.Column(db.String(255))
    Amount = db.Column(db.Float)

    # Relationship if needed, though it might not be necessary for the query
    transaction = db.relationship('Transaction', backref='items')


class Budget(db.Model, BaseMixin):
    __tablename__ = 'Budget'
    Budget_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Amount = db.Column(DECIMAL(10, 2), nullable=False)  # Budget amount
    Notes = db.Column(db.Text, nullable=True)  # Optional description or notes
    Event_ID = db.Column(db.Integer, db.ForeignKey('Event.Event_ID'), nullable=True)  # Linked to Event
    Sub_Event_ID = db.Column(db.Integer, db.ForeignKey('Sub_Event.Sub_Event_ID'), nullable=True)  # Linked to SubEvent
    modified_date = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships with Event and SubEvent
    event = db.relationship('Event', backref='budgets', lazy=True)
    sub_event = db.relationship('SubEvent', backref='budgets', lazy=True)


class Notification(db.Model, BaseMixin):
    __tablename__ = 'Notification'
    Notification_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('User.User_ID'), nullable=False)
    Title = db.Column(db.String(200), nullable=False)
    Message = db.Column(db.Text, nullable=False)
    Type = db.Column(db.String(50), default='info')  # info, success, warning, danger
    Is_Read = db.Column(db.Boolean, default=False)
    Created_At = db.Column(db.DateTime, default=func.current_timestamp())
    Related_Event_ID = db.Column(db.Integer, db.ForeignKey('Event.Event_ID'), nullable=True)
    Related_Transaction_ID = db.Column(db.Integer, db.ForeignKey('transaction_table.Transaction_ID'), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='notifications', lazy=True)
    event = db.relationship('Event', backref='notifications', lazy=True)
    transaction = db.relationship('Transaction', backref='notifications', lazy=True)


class ActivityLog(db.Model, BaseMixin):
    __tablename__ = 'Activity_Log'
    Log_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('User.User_ID'), nullable=False)
    Action = db.Column(db.String(100), nullable=False)  # e.g., 'created', 'updated', 'deleted'
    Entity_Type = db.Column(db.String(50), nullable=False)  # e.g., 'Event', 'Transaction', 'User'
    Entity_ID = db.Column(db.Integer, nullable=True)  # ID of the affected entity
    Description = db.Column(db.Text, nullable=False)
    IP_Address = db.Column(db.String(45), nullable=True)
    Timestamp = db.Column(db.DateTime, default=func.current_timestamp())
    
    # Relationship
    user = db.relationship('User', backref='activity_logs', lazy=True)

