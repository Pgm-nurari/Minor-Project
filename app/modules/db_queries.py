from app import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

def create_entry(model, **kwargs):
    """Dynamically create a new entry in the specified model."""
    try:
        entry = model(**kwargs)
        db.session.add(entry)
        db.session.commit()
        return entry
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating entry:", e)
        return None

def read_entries(model, filters=None, columns=None):
    """Read entries from the specified model with optional filters and selected columns."""
    try:
        query = db.session.query(model)
        
        if columns:
            query = query.with_entities(*[getattr(model, col) for col in columns])
        
        if filters:
            filter_conditions = [getattr(model, key) == value for key, value in filters.items()]
            query = query.filter(and_(*filter_conditions))
        
        return query.all()
    except SQLAlchemyError as e:
        print("Error reading entries:", e)
        return None

def update_entry(model, filters, updates):
    """Update an entry in the specified model based on filters and provided updates."""
    try:
        query = db.session.query(model)
        
        filter_conditions = [getattr(model, key) == value for key, value in filters.items()]
        entry = query.filter(and_(*filter_conditions)).first()
        
        if entry:
            for key, value in updates.items():
                setattr(entry, key, value)
            db.session.commit()
            return entry
        else:
            print("No entry found matching the filters.")
            return None
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error updating entry:", e)
        return None

def delete_entry(model, filters):
    """Delete an entry from the specified model based on filters."""
    try:
        query = db.session.query(model)
        
        filter_conditions = [getattr(model, key) == value for key, value in filters.items()]
        entry = query.filter(and_(*filter_conditions)).first()
        
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return True
        else:
            print("No entry found matching the filters.")
            return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error deleting entry:", e)
        return False

def filter_data(model, filters=None, columns=None):
    """Dynamically filter data from the specified model."""
    return read_entries(model, filters=filters, columns=columns)
