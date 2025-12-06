from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get(self, model, entity_id: int):
        return self.session.query(model).filter(model.id == entity_id).first()

    def list(self, model):
        return self.session.query(model).all()

    def delete(self, entity):
        self.session.delete(entity)
        self.session.commit()

    def update(self, entity, **kwargs):
        """Update fields on an entity and commit."""
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        self.session.commit()
        self.session.refresh(entity)
        return entity
