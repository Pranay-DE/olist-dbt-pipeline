from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

#Project Paths
DBT_PROJECT_DIR = r"C:\Users\mobip\OneDrive\Documents\My Personal\DBT\jlr_pipeline"
DBT_EXECUTABLE = r"C:\Users\mobip\OneDrive\Documents\My Personal\DBT\jlr_pipeline\airflow_env\Scripts\dbt.exe"

#Configuration for all the tasks in this DAG
default_args = {
    'owner': 'pranay',  #Owner of the DAG
    'retries': 1,       # Number of retries in case of failure here it is 1
    'retry_delay': timedelta(minutes=5),    # Delay between retries in case of failure here it is 5 minutes
    'email': ['pranayghadigaonkar1912@gmail.com'],  #Email address to send notifications in case of failure
    'email_on_failure': True,   #Send email notification in case of failure
    'email_on_retry': False     #Send email notification in case of retry
}

#Create the DAG (workflow container)
dag = DAG(
    'olist_dbt_pipeline',   #Name of the DAG
    default_args=default_args,
    description = 'Daily dbt pipeline for olist project',
    schedule_interval = '0 2 * * *',    #Cron expression for scheduling the DAG to run daily at 2 AM
    # 0 is minute, 2 is hour, * is day of month, * is month, * is day of week 
    start_date = days_ago(1), #When to start scheduling
    catchup = False, #Do not run missed dates
    tags=['dbt', 'olist', 'pipeline']  #Tags for categorizing the DAG
)

#Define a task (A single unit of work in the DAG)
dbt_build = BashOperator(
    task_id = 'dbt_build',  #Task Name
    bash_command = f'cd "{DBT_PROJECT_DIR}" && "{DBT_EXECUTABLE}" build',   #What to run in the task, here it is changing directory to the dbt project and running dbt build command
    dag = dag #Which DAG this task belongs to
)  #Execute the task