import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from eralchemy2 import render_er

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(250), nullable=False)
    apellidos = Column(String(250), nullable=False)
    nombre_usuario = Column(String(250), unique=True, nullable=False)
    correo_electronico = Column(String(250), unique=True, nullable=False)
    contrasena = Column(String(250), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    login_status = Column(Boolean, default=False)

    # Relación con Personajes y Planetas favoritos
    personajes_favoritos = relationship("PersonajesFavoritos", back_populates="usuario")
    planetas_favoritos = relationship("PlanetasFavoritos", back_populates="usuario")

class Personaje(Base):
    __tablename__ = 'personaje'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(250), nullable=False)
    apellido = Column(String(250), nullable=True)
    genero = Column(String(50), nullable=False)
    altura = Column(Integer, nullable=True)
    fecha_nacimiento = Column(String(50), nullable=True)
    edad = Column(Integer, nullable=True)
    especie_id = Column(Integer, ForeignKey('especie.id'))
    planeta_origen_id = Column(Integer, ForeignKey('planeta.id'))
    planeta_residencia_id = Column(Integer, ForeignKey('planeta.id'))

    # Relaciones con Especie y Planeta por planeta de orígen y residencia
    especie = relationship("Especie", back_populates="personajes")
    planeta_origen = relationship("Planeta", foreign_keys=[planeta_origen_id], back_populates="personajes_origen")
    planeta_residencia = relationship("Planeta", foreign_keys=[planeta_residencia_id], back_populates="personajes_residencia")

class Especie(Base):
    __tablename__ = 'especie'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(250), nullable=False)

    # Relación con Personaje
    personajes = relationship("Personaje", back_populates="especie")

class Planeta(Base):
    __tablename__ = 'planeta'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(250), nullable=False)
    diametro = Column(Integer, nullable=True)
    terreno_id = Column(Integer, ForeignKey('terreno.id'))
    clima = Column(String(250), nullable=True)
    poblacion = Column(Integer, nullable=True)

    # Relación con Personajes por residencia y planeta de origen. 
    personajes_origen = relationship("Personaje", foreign_keys=[Personaje.planeta_origen_id], back_populates="planeta_origen")
    personajes_residencia = relationship("Personaje", foreign_keys=[Personaje.planeta_residencia_id], back_populates="planeta_residencia")
    residentes = relationship("Personaje", back_populates="planeta_residencia")

    # Relación con Terreno
    terreno = relationship("Terreno", back_populates="planetas")

class Terreno(Base):
    __tablename__ = 'terreno'
    id = Column(Integer, primary_key=True)
    tipo = Column(String(250), nullable=False)

    # Relación con Planeta
    planetas = relationship("Planeta", back_populates="terreno")

class PersonajesFavoritos(Base):
    __tablename__ = 'personajes_favoritos'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    personaje_id = Column(Integer, ForeignKey('personaje.id'))

    # Relación con Usuario y Personaje
    usuario = relationship("Usuario", back_populates="personajes_favoritos")
    personaje = relationship("Personaje")

class PlanetasFavoritos(Base):
    __tablename__ = 'planetas_favoritos'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    planeta_id = Column(Integer, ForeignKey('planeta.id'))

    # Relación con Usuario y Planeta
    usuario = relationship("Usuario", back_populates="planetas_favoritos")
    planeta = relationship("Planeta")

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')

