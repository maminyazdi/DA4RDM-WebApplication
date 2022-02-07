from da4rdm import db
from datetime import datetime

class InflexibleDataSourceConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_server = db.Column(db.String(128))
    db_name = db.Column(db.String(128))
    trusted_connection = db.Column(db.Boolean())
    query = db.Column(db.String(1024))

    def __repr__(self):
        return f'<Connection to database "{self.db_name}" from "{self.db_server}" (sql server))>'

association_table = db.Table('association', db.Model.metadata,
    db.Column('dialect_id', db.Integer, db.ForeignKey('dataBaseDialect.id')),
    db.Column('parameter_id', db.Integer, db.ForeignKey('dialectParameters.id')))

class DataBaseDialect(db.Model):
    __tablename__ = 'dataBaseDialect'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(128))
    parameters = db.relationship("DialectParameters", secondary=association_table)

    def __repr__(self):
        return f'Dialect = {self.name} with ID = {self.id} and Parameters = {self.parameters}'

class DialectParameters(db.Model):
    __tablename__ = 'dialectParameters'
    id       = db.Column(db.Integer, primary_key=True)
    label    = db.Column(db.String(128))

    def __repr__(self):
        return f'Parameter {self.id} = {self.label}'



class DataSourceConnection(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    dialect_id       = db.Column(db.Integer, db.ForeignKey('dataBaseDialect.id'))
    parameter_values = db.Column(db.String(512))




class CopiedFrontendLogs(db.Model):
    __tablename__ = 'frontend_logs'
    Id          = db.Column(db.Integer, primary_key=True)
    Time        = db.Column(db.DateTime)
    AccessToken = db.Column(db.String(255))
    Resource    = db.Column(db.String(444))
    Method      = db.Column(db.String(255))
    Counter     = db.Column(db.Integer)

class CopiedBackendLogs(db.Model):
    __tablename__ = 'backend_logs'
    Id           = db.Column(db.Integer, primary_key=True)
    Time         = db.Column(db.DateTime)
    AccessToken  = db.Column(db.String(255))
    ServiceScope = db.Column(db.String(255))
    Resource     = db.Column(db.String(444))

class ReshapedFrontEndLogs(db.Model):
    __tablename__ = 'reshaped_frontend_logs'
    Id            = db.Column(db.Integer, primary_key=True)
    Time          = db.Column(db.DateTime)
    AccessToken   = db.Column(db.String(255))
    Page          = db.Column(db.String(800))
    Method        = db.Column(db.String(800))
    Rid           = db.Column(db.Integer)

class ReshapedBackEndLogs(db.Model):
    __tablename__ = 'reshaped_backend_logs'
    Id            = db.Column(db.Integer, primary_key=True)
    Time          = db.Column(db.DateTime)
    AccessToken   = db.Column(db.String(255))
    ServiceScope  = db.Column(db.String(255))
    Call          = db.Column(db.String(444))
    Rid           = db.Column(db.String(444))

class DataSource(db.Model):
    __tablename__  = 'data_source'
    Id             = db.Column(db.Integer, primary_key=True)
    Name           = db.Column(db.String(255))
    Type           = db.Column(db.String(255))
    StoredOnServer = db.Column(db.Boolean)
    LastModified   = db.Column(db.DateTime)
    Parameters     = db.Column(db.String(1000))

class SessionInformation(db.Model):
    __tablename__          = 'session_information'
    Id                     = db.Column(db.String(64), primary_key=True)
    UnmodifiedDataLocation = db.Column(db.String(255))
    WorkingDataLocation    = db.Column(db.String(255))
    PDDataLocation         = db.Column(db.String(255))
    EventLogLocation       = db.Column(db.String(255))
    OutputDataLocation     = db.Column(db.String(255))
    PMXesAttributes        = db.Column(db.String(2000))
    PMFilters              = db.Column(db.String(2000))
    PMOptions              = db.Column(db.String(2000))

class SaveConfiguration(db.Model):
    __tablename__          = 'save_configuration'
    Id                     = db.Column(db.Integer, primary_key=True)
    ConfigName                   = db.Column(db.String(255))
    ConfigData                 = db.Column(db.String(255))
    CreatedDate                   = db.Column(db.DateTime, default=datetime.now)

#db.create_all()
