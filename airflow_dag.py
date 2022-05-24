
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from colour_preprocessing import get_colour_names_of_all_images
from feature_extraction import feature_vectors_of_folder
from dim_reduce import get_reduced_features

import os

# ------- set function variables -----------

path = "/GitHub/GraphAesthetics-PreProcessing/"
folder = "investigating-aesthetics"

def colour_values():
    return {
        "path": path,
        "folder": folder,
        "dict_file": "colourNames.csv",
        "n_clstrs": 20
    }

def feature_extraction_values():
    return {
        'folder': path + folder
    }

def pca_values():
    return {
            'zahl': 20,
            'metafolder': path + folder + "_metadata",
            'file': "feature_vectors.csv"
    }

# ----------------- make folder ----------------------

def make_metadata_folder():
    if not os.path.exists(path + folder + "_metadata"):
        os.makedirs(path + folder + "_metadata")
    else:
        print('metadata folder exists')

# -----------------------------------------------------

default_args = {
    'owner': 'Britney Spears',
    'start_date': days_ago(0),
    'email': ['therealbritney@spearsmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# -----------------------------------------------------

with DAG(
    dag_id='Image_Processing',
    default_args=default_args,
    description='Image PreProcessing',
    schedule_interval=timedelta(days=1)
) as dag:

    mkdir_metadata = PythonOperator(
        task_id="mkdir_metadata",
        python_callable=make_metadata_folder
    )

    colour_values_task = PythonOperator(
        task_id="colour_values",
        python_callable=colour_values
    )

    extract_colour_info = PythonOperator(
        task_id="extract_colour_info",
        python_callable=get_colour_names_of_all_images,
        op_kwargs=colour_values_task.output
    )

    fv_values_task = PythonOperator(
        task_id="fv_values",
        python_callable=feature_extraction_values
    )

    extract_feature_vectors = PythonOperator(
        task_id="extract_feature_vectors",
        python_callable=feature_vectors_of_folder,
        op_kwargs=fv_values_task.output
    )

    reduce_task = PythonOperator(
        task_id="reduce_values",
        python_callable=pca_values
    )

    reduce_feature_vectors = PythonOperator(
        task_id="reduce_feature_vectors",
        python_callable=get_reduced_features,
        op_kwargs=reduce_task.output
    )


    mkdir_metadata>>colour_values_task>>extract_colour_info
    mkdir_metadata>>fv_values_task>>extract_feature_vectors>>reduce_task>>reduce_feature_vectors

# -----------------------------------------------------
