from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="team")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
        }


class Captain(Base):
    __tablename__ = 'captain'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    date = Column(DateTime, nullable=False)
    role = Column(String(20))
    runs = Column(Integer())
    wickets = Column(Integer())
    description = Column(String(250))
    image = Column(String(250))
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship(
               Team, backref=backref('captain', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="captain")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'role': self.role,
            'runs' : self.runs,
            'wickets' : self.wickets,
            'description': self.description,
            'image': self.image,
            'team': self.team.name
        }


engine = create_engine('sqlite:///team.db')

Base.metadata.create_all(engine)
