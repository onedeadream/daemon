from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from config import URL_DATABASE

Base = declarative_base()
engine = create_engine(URL_DATABASE)
connection = engine.connect()


class List_Hosts(Base):
    __tablename__ = 'list_hosts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_name = Column(VARCHAR(255), nullable=False)
    ip_address = Column(VARCHAR(255), nullable=False)
    mac_address = Column(VARCHAR(255), nullable=False)
    system_info = relationship("System_Info", back_populates="host")
    monitoring_systems = relationship("Monitoring_System", back_populates="host")


class System_Info(Base):
    __tablename__ = 'system_info'
    id = Column(Integer, primary_key=True)
    proc_name = Column(VARCHAR(255), nullable=False)
    freq_proc = Column(VARCHAR(255))
    gpu_name = Column(VARCHAR(255), nullable=False)
    gpu_memory = Column(FLOAT)
    total_memory = Column(FLOAT)
    total_virtual_memory = Column(FLOAT)
    hosts_id = Column(ForeignKey('list_hosts.id'))
    host = relationship("List_Hosts", back_populates="system_info")


class Monitoring_System(Base):
    __tablename__ = 'monitoring_system'
    id = Column(Integer, primary_key=True)
    cpu_percent = Column(ARRAY(String))
    gpu_percent = Column(ARRAY(String))
    used_virtual_memory = Column(ARRAY(String))
    temperature_gpu = Column(ARRAY(String))
    used_disk = Column(ARRAY(String))
    time_monitoring = Column(ARRAY(String))
    host_id = Column(ForeignKey('list_hosts.id'))
    host = relationship("List_Hosts", back_populates="monitoring_systems")


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR)
    password = Column(VARCHAR)
    role = Column(VARCHAR)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session(autoflush=True)
session.autoflush = True
