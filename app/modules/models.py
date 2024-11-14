from app import db

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
    modified_date = db.Column(db.DateTime, default=db.func.current_timestamp())

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
    modified_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships to User, EventType, Department, and Event models
    sub_event_manager = db.relationship('User', foreign_keys=[Sub_Event_Manager], backref='sub_events_managed', lazy=True)
    event_type = db.relationship('EventType', backref='sub_events', lazy=True)
    department = db.relationship('Department', backref='sub_events', lazy=True)
    event = db.relationship('Event', backref='sub_events', lazy=True)

