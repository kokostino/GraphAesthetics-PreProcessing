
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from colour_preprocessing import get_colour_names_of_all_images


def colour_values():
    return {
        "path": "/GitHub/GraphAesthetics-PreProcessing/",
        "folder": "investigating-aesthetics/",
        "dict_file": "colourNames.csv",
        "n_clstrs": 20
    }

default_args = {
    'owner': 'Britney Spears',
    'start_date': days_ago(0),
    'email': ['therealbritney@spearsmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='Image_Processing',
    default_args=default_args,
    description='Image PreProcessing',
    schedule_interval=timedelta(days=1)
) as dag:

    colour_values_task = PythonOperator(
        task_id="colour_values",
        python_callable=colour_values
    )

    extract_colour_info = PythonOperator(
        task_id="extract_colour_info",
        python_callable=get_colour_names_of_all_images,
        op_kwargs=colour_values_task.output
    )


    colour_values_task>>extract_colour_info
