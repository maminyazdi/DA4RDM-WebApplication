import os
#from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    #############
    ### flask ###
    #############
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'G01VLn8sy9uPdXgP48pH'

    ################
    ### database ###
    ################
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ###########################
    ### project directories ###
    ###########################
    USER_PROJECT_DIRECTORY = os.environ.get('USER_PROJ_DIR') or './da4ds/user_projects/'

    ###################################
    ### temporary storage directory ###
    ###################################
    TEMP_STORAGE_DIRECTORY = os.environ.get('TEMP_STORAGE_DIR') or './da4ds/temporary_results/'

    ##########################
    ### output directories ###
    ##########################
    CSV_STORAGE_DIRECTORY = os.environ.get('OUTPUT_DIR') or 'C:/Temp'
