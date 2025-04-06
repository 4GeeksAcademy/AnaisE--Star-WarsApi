from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import ARRAY, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    favorites = relationship('Favorite', back_populates='user')

class Film(Base):
    __tablename__ = 'film'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    director = Column(String(250))
    producer = Column(String(250))
    episode_id = Column(Integer)
    opening_crawl = Column(String(500))
    release_date = Column(String(50))
    url = Column(String(250))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    characters = relationship('Character', secondary='film_character', back_populates='films')

class Character(Base):
    __tablename__ = 'character'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    birth_year = Column(String(50))
    eye_color = Column(String(50))
    gender = Column(String(50))
    hair_color = Column(String(50))
    height = Column(Integer)
    mass = Column(Numeric)
    skin_color = Column(String(50))
    homeworld_id = Column(Integer, ForeignKey('planet.id'))
    url = Column(String(250))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    homeworld = relationship('Planet', back_populates='residents')
    films = relationship('Film', secondary='film_character', back_populates='characters')
    species = relationship('Specie', secondary='character_specie', back_populates='characters')
    favorites = relationship('Favorite', back_populates='character')

class Specie(Base):
    __tablename__ = 'specie'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    classification = Column(String(250))
    designation = Column(String(250))
    average_height = Column(Numeric)
    average_lifespan = Column(Integer)
    eye_colors = Column(String(250))
    hair_colors = Column(String(250))
    skin_colors = Column(String(250))
    language = Column(String(250))
    homeworld_id = Column(Integer, ForeignKey('planet.id'))
    url = Column(String(250))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    homeworld = relationship('Planet')
    characters = relationship('Character', secondary='character_specie', back_populates='species')
    films = relationship('Film', secondary='film_specie', back_populates='species')

class Planet(Base):
    __tablename__ = 'planet'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    diameter = Column(Numeric)
    rotation_period = Column(Integer)
    orbital_period = Column(Integer)
    gravity = Column(String(50))
    population = Column(Numeric)
    climate = Column(String(250))
    terrain = Column(String(250))
    surface_water = Column(Numeric)
    url = Column(String(250))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    residents = relationship('Character', back_populates='homeworld')
    species = relationship('Specie', back_populates='homeworld')
    films = relationship('Film', secondary='film_planet', back_populates='planets')
    favorites = relationship('Favorite', back_populates='planet')

class Vehicle(Base):
    __tablename__ = 'vehicle'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    vehicle_class = Column(String(100), nullable=False)
    manufacturer = Column(String(250))
    length = Column(Numeric)
    cost_in_credits = Column(String(50))
    crew = Column(String(50))
    passengers = Column(String(50))
    max_atmosphering_speed = Column(String(50))
    cargo_capacity = Column(Numeric)
    consumables = Column(String(100))
    url = Column(String(250))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    pilots = relationship('Character', secondary='vehicle_pilot', back_populates='vehicles')
    favorites = relationship('Favorite', back_populates='vehicle')

class Favorite(Base):
    __tablename__ = 'favorite'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    character_id = Column(Integer, ForeignKey('character.id'), nullable=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=True)
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), nullable=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    
    user = relationship('User', back_populates='favorites')
    character = relationship('Character', back_populates='favorites')
    planet = relationship('Planet', back_populates='favorites')
    vehicle = relationship('Vehicle', back_populates='favorites')

# Tablas de asociación para relaciones many-to-many
class FilmCharacter(Base):
    __tablename__ = 'film_character'
    film_id = Column(Integer, ForeignKey('film.id'), primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)

class CharacterSpecie(Base):
    __tablename__ = 'character_specie'
    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)
    specie_id = Column(Integer, ForeignKey('specie.id'), primary_key=True)

class FilmSpecie(Base):
    __tablename__ = 'film_specie'
    film_id = Column(Integer, ForeignKey('film.id'), primary_key=True)
    specie_id = Column(Integer, ForeignKey('specie.id'), primary_key=True)

class FilmPlanet(Base):
    __tablename__ = 'film_planet'
    film_id = Column(Integer, ForeignKey('film.id'), primary_key=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), primary_key=True)

class VehiclePilot(Base):
    __tablename__ = 'vehicle_pilot'
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), primary_key=True)
    pilot_id = Column(Integer, ForeignKey('character.id'), primary_key=True)

# Generar el diagrama ER
render_er(Base, 'starwars_erd.png')