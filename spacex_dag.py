from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2005, 1, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("spacex", default_args=default_args, schedule_interval="0 0 1 1 *")

rkt = ['all', 'falcon1', 'falcon9', 'falconheavy']
for i in rkt:
    t1 = BashOperator(
        task_id="get_data_"+i, 
        bash_command="python3 /root/airflow/dags/spacex/load_launches.py -y {{{{ execution_date.year }}}} {} -o /var/data/".format('-r '+i if i!='all' else ''), 
        dag=dag
    )
    
    t2 = BashOperator(
        task_id="print_data_"+i, 
        bash_command="cat /var/data/year={{{{ execution_date.year }}}}/rocket={}/data.csv".format(i), 
        #params={"rocket": i}, # falcon1/falcon9/falconheavy
        dag=dag
    )
    
    t1 >> t2
