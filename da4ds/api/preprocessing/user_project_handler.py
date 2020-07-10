import os
import re
import importlib

def get_all_user_projects(projects_path):
    if projects_path[-1] != '/':
        projects_path += '/'
    dirs = os.listdir(projects_path)
    projects_directories = [str(x) for x in dirs if (os.path.isdir(projects_path + x) and x != '__pycache__')]
    return projects_directories

def import_project_module(project_path, project_name):
    module_name = "." + project_name
    if project_path[-1] == "/":
        project_path = project_path[0:-1]
    package_name = project_path.replace("/", ".")
    package_name = re.sub(r"^\.*", "", package_name) #replace leading and traling dots
    package_name = re.sub(r"\.*$", "", package_name)

    project = importlib.import_module(module_name, package_name)
    return project

def run_user_project(project, session, database, pipeline_parameters):

    project_config = project.init(session, database, pipeline_parameters)

    result_dataframe = project.run(project_config)


    return result_dataframe
