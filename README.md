# DA4RDM Web Application

## Overview
DA4RDM is a robust Web Application designed to facilitate seamless interaction and engagement with the DA4RDM system. With an intuitive user interface and powerful backend functionalities, it provides an efficient platform for users to explore and utilize the features of DA4RDM effortlessly.

## Key Features
- **User-Friendly Interface:** Designed with users in mind, providing an intuitive and seamless user experience.
- **Robust Backend:** Powerful backend functionalities that ensure efficient and reliable performance.
- **Docker Integration:** Easily accessible and deployable using Docker technology for containerized applications.

## Getting Started
### Prerequisites
- Ensure that Docker is installed on your system. If not, download and install it from the [official Docker website](https://www.docker.com/).

### Pulling from Docker Hub
DA4RDM Web Application can be effortlessly pulled from Docker Hub and deployed on any system with Docker support. Use the following command to pull the Docker image:

```bash
docker pull da4rdm/da4rdm
```

----

## Dependencies:
If you want to use anaconda/miniconda, you can (and should) import the following environment.yml from the repository top level. To do this, from your anaconda prompt (in administrator mode) you can enter (with environment.yml pointing to the right file):
> conda env create -f environment.yml

If you use anaconda distribution and hope that everythig will work, you should install flask_sqlalchemy from conda-forge:
> conda install -c conda-forge flask-sqlalchemy

in anaconda prompt. Do the same for flask_migrate and flask_socketio:

> conda install -c conda-forge flask-migrate

> conda install -c conda-forge flask-socketio

It may happen that you need to manually install pip dependencies, which at the time of writing were only [pm4py](https://pypi.org/project/pm4py/) and [graphviz](https://pypi.org/project/graphviz-python/).

Additionally, if you get error frmo graphviz, you may need to install the [graphviz executables](https://graphviz.gitlab.io/download/)  manually to your machine and add the path to them to your path environment variable.


### To run the local development server, set environment variables:

Loading the environment "da4rdm" should already register the environment variables required to run the server. If that seems to not be the case, add them manually. Under powershell:

> $env:FLASK_APP = "da4rdm"
> $env:FLASK_ENV = "development"
> flask run

If you are running on comand shell or anaconda prompt, use these commands instead:
> set FLASK_APP=da4rdm
> set FLASK_ENV=development
> flask run

### Debugging in VSCode

Starting Visual Studio Code from the Anaconda command prompt, everything you need to start debugging should be in place. Make sure, that the correct interpreter is selected. It should be configured to the anaconda environment that contains all the modules needed for this application (i.e. if you perform all the install steps above in the "base" environment, select the anaconda:'base' python interpreter).

Then you should be able to start debugging from the debug activity tab.

## Database and Migrations

ORM used for database connections is [flask-SQLAlchemy](https://www.sqlalchemy.org/).

### Initialize the database
We use the extension [flask-migrate](https://anaconda.org/conda-forge/flask-migrate) which wraps alembic to initialize the database and execute migrations.

The initial setup can be run using
> flask db init

Usually this should not be neccessary as the working version of the current migrations will be provided in the current version of the repository.

Updating the Database via new migrations can be done by simply adding the new classes for the desired model to the models.py in the app repository. Then run
> flask db migrate -m <STRING: description>

check if the changes are detected, then run
> flask db upgrade

## How to Use

The typical use case will be comprised of the following three steps:
1) Selecting a Data Source.
2) Running a data cleaning pipeline.
3) Running the process discovery algorithms.

### Selecting a Data Source

As a first step, your data source should be selected. If you did not prevously select the desired data source, head to Data Initialization -> Save a new data source. Your data source needs an arbitrary name and some parameters. Parameters should be separated by semicolon (;), and values of parameters should be added following the parameter after a definition symbol (:=).
Currently used parameters are path:= and separator:= for CSV files and connection_string:= and query:= for database connections, where connection_string should be a string that can be used by sqlalchemy to create a database engine and connect to the specified database.

Once the connection is stored, you can select it under Data Initialization -> Select data source. After this step has been completed, the data will be stored in a workable form on the server and can be used in the cleaning pipelines and process discovery steps.


### Running a Cleaning Pipeline



### Running the Process Discovery Algorithms


---

## Setting up custom projects

### Adding a project
You can add custom projects to the application which can be seelected from the main view.
By default, custom projects are being placed in the user_projects directory inside of the da4rdm directory. This path can be changed in the configuration.
A custom project should contain a __init__.py file which takes care of all required global imports needed in the project, as well as loading the project specific configuration files. The __init__.py will be the first file to be loaded and is required for the project to be imported into the application.

### Accessing the Data from the Data Source

The initialization function of your project will recieve the session information of your current project. This information contains, amongst other, the location of the data that has been stored after you selected your data source. You can access it by callng

> session_information["unmodified_data_location"]

### Structuring your project
Ideally a custom project is segrated into the execution and pipilening of modules that each serve a specific purpose inside of that pipeline. The intended use of the programme is to have the data pre-processing being done on temporary DASK dataframes for as long as possible.
Some frequently used modules can be found in ./da4rdm/processing_libraries/da4rdm. These include modules for reading data from csv files or databases into DASK dataframes or storing data as csv files, as well as modules for replacing columnar values or column names and such.
You may also extend that library or add your own libraries there.
Modules should adhere to the following interface: func(dataframe, options{args*}) -> {dataframe, additional_results'}.

### Output formats
Your project must return a dataframe object. It should return the results of the pipeline. The dataframe will be stored at

> session_information["data_location"]

so that the process discovery can find the cleaned data.

You can store dataframes as CSV-File by including the corresponding module. The output-path for these files can be specified in the config.py of your project.
The final result of the pipeline can be shown on the application front end. This expects a json response object that can also be created by the corresponding module. The frontend at the moments can display only text. The parameter you give to that modules should thus for now only have the value "text". In the future it is planned to support displaying graphs for data. In this case, the parameter should have the value "table".


---
### Working with DA4RDM UI
- Use the example data available in the SampleData folder (use the latest csv file)
- Go to "Data Pre-processing" tab
- Use the + button in "Data Source" section
- Give any name to "Datasource name" field
- Select CSV file format from the set of radio buttons
- Select your local file (sample data)
- Press Save
- Select the data source from the dropdown list within the "Data Source" section and press Checkmark button
- From the "Data Pre-processing Pipeline" section, select "Process_Discovery" within the dropdown and press Checkmark button
- Click on Run project
- You get redirected to the "Process Analysis" tab
- In "Event Log" section, 
    - Select Timestamp as "Timestamp"
    - Select Case ID as "User Id"
    - Select Activity as "Operation"
    - Submit
- Within Options section, click on the Play button (blue color) to run the algorithm and produce a process model._


