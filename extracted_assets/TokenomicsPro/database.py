import os
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

# Get database URL from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    avatar_initials = Column(String(10))
    plan = Column(String(20), default='free', nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tokenomics_models = relationship("TokenomicsModel", back_populates="user", cascade="all, delete-orphan")
    crypto_systems = relationship("CryptoeconomicSystem", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password):
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'display_name': self.display_name,
            'avatar_initials': self.avatar_initials,
            'plan': self.plan,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Web3 StartupBuilder Models
class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default='draft')  # draft, in_progress, completed
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    last_edited = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    token_design_progress = Column(Integer, default=0)
    team_members = Column(JSON, default=lambda: [])
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    token = relationship("Token", back_populates="project", uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'user_id': self.user_id,
            'last_edited': self.last_edited.isoformat() if self.last_edited else None,
            'token_design_progress': self.token_design_progress,
            'team_members': self.team_members,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Token(Base):
    __tablename__ = 'tokens'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(100), nullable=False)
    symbol = Column(String(10), nullable=False)
    type = Column(String(20), nullable=False)  # ERC-20, ERC-721, etc.
    total_supply = Column(String(100), nullable=False)
    initial_price = Column(String(100))
    initial_market_cap = Column(String(100))
    circulating_supply = Column(String(100))
    distribution = Column(JSON, default=lambda: {})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="token")
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'symbol': self.symbol,
            'type': self.type,
            'total_supply': self.total_supply,
            'initial_price': self.initial_price,
            'initial_market_cap': self.initial_market_cap,
            'circulating_supply': self.circulating_supply,
            'distribution': self.distribution,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Resource(Base):
    __tablename__ = 'resources'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String(20), nullable=False)  # guide, tutorial, case_study
    image_background = Column(String(50), nullable=False)
    image_icon = Column(String(50), nullable=False)
    link = Column(String(255), nullable=False)
    link_text = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'image_background': self.image_background,
            'image_icon': self.image_icon,
            'link': self.link,
            'link_text': self.link_text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# TokenomicsLab Models
class TokenomicsModel(Base):
    __tablename__ = 'tokenomics_models'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    model_type = Column(String(20), default='base')  # base, utility, governance
    total_supply = Column(Integer, nullable=False)
    distribution = Column(JSON, default=lambda: {})
    vesting_schedules = Column(JSON, default=lambda: {})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional fields for specific model types
    initial_users = Column(Integer)
    user_growth_rate = Column(Float)
    initial_staking_rate = Column(Float)
    staking_apy = Column(Float)
    
    # Extended data stored as JSON
    data = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="tokenomics_models")
    
    def to_dict(self):
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'model_type': self.model_type,
            'total_supply': self.total_supply,
            'distribution': self.distribution,
            'vesting_schedules': self.vesting_schedules,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'data': self.data
        }
        
        # Add model-specific fields
        if self.model_type == 'utility':
            result.update({
                'initial_users': self.initial_users,
                'user_growth_rate': self.user_growth_rate
            })
        elif self.model_type == 'governance':
            result.update({
                'initial_staking_rate': self.initial_staking_rate,
                'staking_apy': self.staking_apy
            })
            
        return result

class CryptoeconomicSystem(Base):
    __tablename__ = 'cryptoeconomic_systems'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # System data stored as JSON
    data = Column(JSON, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="crypto_systems")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'data': self.data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TokenomicsComparison(Base):
    __tablename__ = 'tokenomics_comparisons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    model_ids = Column(JSON, default=lambda: [])  # Array of tokenomics model IDs
    parameters = Column(JSON, default=lambda: {})  # Comparison parameters
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'model_ids': self.model_ids,
            'parameters': self.parameters,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Create all tables
def init_db():
    Base.metadata.create_all(engine)
    
    # Create an admin user if one doesn't exist
    session = Session()
    admin = session.query(User).filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@tokenomicslab.com',
            display_name='Administrator',
            avatar_initials='AD',
            plan='premium',
            is_admin=True
        )
        admin.set_password('admin123')  # Default password, should be changed
        session.add(admin)
        
        # Create a demo user
        demo = User(
            username='demo',
            email='demo@tokenomicslab.com',
            display_name='Demo User',
            avatar_initials='DU',
            plan='free',
            is_admin=False
        )
        demo.set_password('demo123')
        session.add(demo)
        
        # Create initial resources
        resources = [
            Resource(
                title="Getting Started with Tokenomics",
                description="Learn the basics of tokenomics and how to design an effective token model",
                type="guide",
                image_background="bg-gradient-to-r from-blue-500 to-purple-500",
                image_icon="📚",
                link="/guides/tokenomics-basics",
                link_text="Read Guide"
            ),
            Resource(
                title="Token Distribution Best Practices",
                description="Explore strategies for optimal token distribution and allocation",
                type="tutorial",
                image_background="bg-gradient-to-r from-green-500 to-teal-500",
                image_icon="🔄",
                link="/tutorials/token-distribution",
                link_text="View Tutorial"
            ),
            Resource(
                title="Cryptoeconomic System Design",
                description="Deep dive into designing robust cryptoeconomic systems with proper incentives",
                type="case_study",
                image_background="bg-gradient-to-r from-purple-500 to-pink-500",
                image_icon="🧮",
                link="/case-studies/cryptoeconomics",
                link_text="Explore"
            )
        ]
        
        for resource in resources:
            session.add(resource)
        
        session.commit()
    session.close()

# Database utility functions
def get_user_by_username(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user

def get_user_by_id(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    return user

def get_all_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return users

def create_user(username, email, password, display_name=None, is_admin=False, plan='free'):
    session = Session()
    
    if display_name is None:
        display_name = username
        
    avatar_initials = ''.join([name[0].upper() for name in display_name.split()[:2]])
    
    user = User(
        username=username, 
        email=email, 
        display_name=display_name,
        avatar_initials=avatar_initials,
        plan=plan,
        is_admin=is_admin
    )
    user.set_password(password)
    
    session.add(user)
    try:
        session.commit()
        new_user = session.query(User).filter_by(username=username).first()
        session.close()
        return new_user
    except:
        session.rollback()
        session.close()
        return None

def update_user(user_id, **kwargs):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    
    if not user:
        session.close()
        return None
    
    for key, value in kwargs.items():
        if key == 'password':
            user.set_password(value)
        elif hasattr(user, key):
            setattr(user, key, value)
    
    try:
        session.commit()
        updated_user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return updated_user
    except:
        session.rollback()
        session.close()
        return None

# Project functions
def create_project(name, user_id):
    session = Session()
    project = Project(
        name=name,
        user_id=user_id,
        status="draft",
        token_design_progress=0,
        team_members=[]
    )
    session.add(project)
    try:
        session.commit()
        new_project = session.query(Project).filter_by(id=project.id).first()
        session.close()
        return new_project
    except:
        session.rollback()
        session.close()
        return None

def get_project_by_id(project_id):
    session = Session()
    project = session.query(Project).filter_by(id=project_id).first()
    session.close()
    return project

def get_projects_by_user(user_id):
    session = Session()
    projects = session.query(Project).filter_by(user_id=user_id).all()
    session.close()
    return projects

def get_all_projects():
    session = Session()
    projects = session.query(Project).all()
    session.close()
    return projects

def update_project(project_id, **kwargs):
    session = Session()
    project = session.query(Project).filter_by(id=project_id).first()
    
    if not project:
        session.close()
        return None
    
    for key, value in kwargs.items():
        if hasattr(project, key):
            setattr(project, key, value)
    
    try:
        session.commit()
        updated_project = session.query(Project).filter_by(id=project_id).first()
        session.close()
        return updated_project
    except:
        session.rollback()
        session.close()
        return None

def delete_project(project_id):
    session = Session()
    project = session.query(Project).filter_by(id=project_id).first()
    
    if not project:
        session.close()
        return False
    
    try:
        session.delete(project)
        session.commit()
        session.close()
        return True
    except:
        session.rollback()
        session.close()
        return False

# Token functions
def create_token(project_id, name, symbol, token_type, total_supply, **kwargs):
    session = Session()
    token = Token(
        project_id=project_id,
        name=name,
        symbol=symbol,
        type=token_type,
        total_supply=total_supply,
        **kwargs
    )
    session.add(token)
    try:
        session.commit()
        new_token = session.query(Token).filter_by(id=token.id).first()
        session.close()
        return new_token
    except:
        session.rollback()
        session.close()
        return None

def get_token_by_project_id(project_id):
    session = Session()
    token = session.query(Token).filter_by(project_id=project_id).first()
    session.close()
    return token

def update_token(token_id, **kwargs):
    session = Session()
    token = session.query(Token).filter_by(id=token_id).first()
    
    if not token:
        session.close()
        return None
    
    for key, value in kwargs.items():
        if hasattr(token, key):
            setattr(token, key, value)
    
    try:
        session.commit()
        updated_token = session.query(Token).filter_by(id=token_id).first()
        session.close()
        return updated_token
    except:
        session.rollback()
        session.close()
        return None

# Resource functions
def get_resources():
    session = Session()
    resources = session.query(Resource).all()
    session.close()
    return resources

def get_resource_by_id(resource_id):
    session = Session()
    resource = session.query(Resource).filter_by(id=resource_id).first()
    session.close()
    return resource

def create_resource(title, description, resource_type, image_background, image_icon, link, link_text):
    session = Session()
    resource = Resource(
        title=title,
        description=description,
        type=resource_type,
        image_background=image_background,
        image_icon=image_icon,
        link=link,
        link_text=link_text
    )
    session.add(resource)
    try:
        session.commit()
        new_resource = session.query(Resource).filter_by(id=resource.id).first()
        session.close()
        return new_resource
    except:
        session.rollback()
        session.close()
        return None

# TokenomicsModel functions
def create_tokenomics_model(name, description, user_id, model_type, total_supply, **kwargs):
    session = Session()
    model = TokenomicsModel(
        name=name,
        description=description,
        user_id=user_id,
        model_type=model_type,
        total_supply=total_supply,
        **kwargs
    )
    session.add(model)
    try:
        session.commit()
        new_model = session.query(TokenomicsModel).filter_by(id=model.id).first()
        session.close()
        return new_model
    except:
        session.rollback()
        session.close()
        return None

def get_tokenomics_models_by_user(user_id):
    session = Session()
    models = session.query(TokenomicsModel).filter_by(user_id=user_id).all()
    session.close()
    return models

def get_all_tokenomics_models():
    session = Session()
    models = session.query(TokenomicsModel).all()
    session.close()
    return models

def get_tokenomics_model_by_id(model_id):
    session = Session()
    model = session.query(TokenomicsModel).filter_by(id=model_id).first()
    session.close()
    return model

def update_tokenomics_model(model_id, **kwargs):
    session = Session()
    model = session.query(TokenomicsModel).filter_by(id=model_id).first()
    
    if not model:
        session.close()
        return None
    
    for key, value in kwargs.items():
        if hasattr(model, key):
            setattr(model, key, value)
    
    try:
        session.commit()
        updated_model = session.query(TokenomicsModel).filter_by(id=model_id).first()
        session.close()
        return updated_model
    except:
        session.rollback()
        session.close()
        return None

def delete_tokenomics_model(model_id):
    session = Session()
    model = session.query(TokenomicsModel).filter_by(id=model_id).first()
    
    if not model:
        session.close()
        return False
    
    try:
        session.delete(model)
        session.commit()
        session.close()
        return True
    except:
        session.rollback()
        session.close()
        return False

# CryptoeconomicSystem functions
def create_cryptoeconomic_system(name, description, user_id, data):
    session = Session()
    system = CryptoeconomicSystem(
        name=name,
        description=description,
        user_id=user_id,
        data=data
    )
    session.add(system)
    try:
        session.commit()
        new_system = session.query(CryptoeconomicSystem).filter_by(id=system.id).first()
        session.close()
        return new_system
    except:
        session.rollback()
        session.close()
        return None

def get_cryptoeconomic_systems_by_user(user_id):
    session = Session()
    systems = session.query(CryptoeconomicSystem).filter_by(user_id=user_id).all()
    session.close()
    return systems

def get_all_cryptoeconomic_systems():
    session = Session()
    systems = session.query(CryptoeconomicSystem).all()
    session.close()
    return systems

def get_cryptoeconomic_system_by_id(system_id):
    session = Session()
    system = session.query(CryptoeconomicSystem).filter_by(id=system_id).first()
    session.close()
    return system

def update_cryptoeconomic_system(system_id, **kwargs):
    session = Session()
    system = session.query(CryptoeconomicSystem).filter_by(id=system_id).first()
    
    if not system:
        session.close()
        return None
    
    for key, value in kwargs.items():
        if hasattr(system, key):
            setattr(system, key, value)
    
    try:
        session.commit()
        updated_system = session.query(CryptoeconomicSystem).filter_by(id=system_id).first()
        session.close()
        return updated_system
    except:
        session.rollback()
        session.close()
        return None

def delete_cryptoeconomic_system(system_id):
    session = Session()
    system = session.query(CryptoeconomicSystem).filter_by(id=system_id).first()
    
    if not system:
        session.close()
        return False
    
    try:
        session.delete(system)
        session.commit()
        session.close()
        return True
    except:
        session.rollback()
        session.close()
        return False

# TokenomicsComparison functions
def create_tokenomics_comparison(name, description, user_id, model_ids, parameters=None):
    session = Session()
    comparison = TokenomicsComparison(
        name=name,
        description=description,
        user_id=user_id,
        model_ids=model_ids,
        parameters=parameters or {}
    )
    session.add(comparison)
    try:
        session.commit()
        new_comparison = session.query(TokenomicsComparison).filter_by(id=comparison.id).first()
        session.close()
        return new_comparison
    except:
        session.rollback()
        session.close()
        return None

def get_tokenomics_comparisons_by_user(user_id):
    session = Session()
    comparisons = session.query(TokenomicsComparison).filter_by(user_id=user_id).all()
    session.close()
    return comparisons

def get_tokenomics_comparison_by_id(comparison_id):
    session = Session()
    comparison = session.query(TokenomicsComparison).filter_by(id=comparison_id).first()
    session.close()
    return comparison

def update_tokenomics_comparison(comparison_id, **kwargs):
    session = Session()
    comparison = session.query(TokenomicsComparison).filter_by(id=comparison_id).first()
    
    if not comparison:
        session.close()
        return None
    
    for key, value in kwargs.items():
        if hasattr(comparison, key):
            setattr(comparison, key, value)
    
    try:
        session.commit()
        updated_comparison = session.query(TokenomicsComparison).filter_by(id=comparison_id).first()
        session.close()
        return updated_comparison
    except:
        session.rollback()
        session.close()
        return None

def delete_tokenomics_comparison(comparison_id):
    session = Session()
    comparison = session.query(TokenomicsComparison).filter_by(id=comparison_id).first()
    
    if not comparison:
        session.close()
        return False
    
    try:
        session.delete(comparison)
        session.commit()
        session.close()
        return True
    except:
        session.rollback()
        session.close()
        return False

# Initialize the database
if __name__ == '__main__':
    init_db()