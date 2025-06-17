from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Enum as PgEnum
from database import Base
from enum import Enum as PyEnum

# Enum for supervisor roles
class SupervisorRoleEnum(PyEnum):
    masters_director = "masters_director"
    internship_manager = "internship_manager"
    researcher = "researcher"

# Table University
class University(Base):
    __tablename__ = 'university'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    website = Column(String(255), nullable=True)

    supervisors = relationship("InternshipSupervisor", back_populates="university")

# Table InternshipSupervisor
class InternshipSupervisor(Base):
    __tablename__ = 'internship_supervisor'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    role = Column(PgEnum(SupervisorRoleEnum), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    university_id = Column(Integer, ForeignKey('university.id'))

    university = relationship("University", back_populates="supervisors")
    internships = relationship("Internship", back_populates="supervisor")

# Table Discipline (recursive)
class Discipline(Base):
    __tablename__ = 'discipline'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey('discipline.id'), nullable=True)

    # Recursive relationships: a discipline can have many subdisciplines (children) 
    # and optionally a parent discipline.
    children = relationship("Discipline", backref=backref("parent", remote_side=[id]))
    
    # Association with Internship through the link table
    internship_links = relationship("InternshipDiscipline", back_populates="discipline", cascade="all, delete-orphan")


class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=False)
    internship_id = Column(Integer, ForeignKey("internship.id", ondelete="CASCADE"))

    internship = relationship("Internship", back_populates="keywords")


class Internship(Base):
    __tablename__ = 'internship'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=True)
    pdf_path = Column(String(255), nullable=True)
    supervisor_id = Column(Integer, ForeignKey('internship_supervisor.id'))

    supervisor = relationship("InternshipSupervisor", back_populates="internships")
    
    disciplines = relationship("InternshipDiscipline", back_populates="internship", cascade="all, delete-orphan")
    keywords = relationship("Keyword", back_populates="internship", cascade="all, delete-orphan")



# Association Table between Internship and Discipline
class InternshipDiscipline(Base):
    __tablename__ = 'internship_discipline'

    internship_id = Column(Integer, ForeignKey('internship.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    discipline_id = Column(Integer, ForeignKey('discipline.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

    internship = relationship("Internship", back_populates="disciplines")
    discipline = relationship("Discipline", back_populates="internship_links")
