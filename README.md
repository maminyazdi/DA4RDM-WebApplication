# DA4DS

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

Loading the environment "da4ds" should already register the environment variables required to run the server. If that seems to not be the case, add them manually. Under powershell:

> $env:FLASK_APP = "da4ds"
> $env:FLASK_ENV = "development"
> flask run

If you are running on comand shell or anaconda prompt, use these commands instead:
> set FLASK_APP=da4ds
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

### Selecitn a Data Source

As a first step, your data source should be selected. If you did not prevously select the desired data source, head to Data Initialization -> Save a new data source. Your data source needs an arbitrary name and some parameters. Parameters should be separated by semicolon (;), and values of parameters should be added following the parameter after a definition symbol (:=).
Currently used parameters are path:= and separator:= for CSV files and connection_string:= and query:= for database connections, where connection_string should be a string that can be used by sqlalchemy to create a database engine and connect to the specified database.

Once the connection is stored, you can select it under Data Initialization -> Select data source. After this step has been completed, the data will be stored in a workable form on the server and can be used in the cleaning pipelines and process discovery steps.


### Running a Cleaning Pipeline



### Rnning the Process Discovery Algorithms





---

## Setting up custom projects

### Adding a project
You can add custom projects to the application which can be seelected from the main view.
By default, custom projects are being placed in the user_projects directory inside of the da4ds directory. This path can be changed in the configuration.
A custom project should contain a __init__.py file which takes care of all required global imports needed in the project, as well as loading the project specific configuration files. The __init__.py will be the first file to be loaded and is required for the project to be imported into the application.

### Accessing the Data from the Data Source

The initialization function of your project will recieve the session information of your current project. This information contains, amongst other, the location of the data that has been stored after you selected your data source. You can access it by callng

> session_information["unmodified_data_location"]

### Structuring your project
Ideally a custom project is segrated into the execution and pipilening of modules that each serve a specific purpose inside of that pipeline. The intended use of the programme is to have the data pre-processing being done on temporary DASK dataframes for as long as possible.
Some frequently used modules can be found in ./da4ds/processing_libraries/da4ds. These include modules for reading data from csv files or databases into DASK dataframes or storing data as csv files, as well as modules for replacing columnar values or column names and such.
You may also extend that library or add your own libraries there.
Modules should adhere to the following interface: func(dataframe, options{args*}) -> {dataframe, additional_results'}.

### Output formats
Your project must return a dataframe object. It should return the results of the pipeline. The dataframe will be stored at

> session_information["data_location"]

so that the process discovery can find the cleaned data.

You can store dataframes as CSV-File by including the corresponding module. The output-path for these files can be specified in the config.py of your project.
The final result of the pipeline can be shown on the application front end. This expects a json response object that can also be created by the corresponding module. The frontend at the moments can display only text. The parameter you give to that modules should thus for now only have the value "text". In the future it is planned to support displaying graphs for data. In this case, the parameter should have the value "table".
