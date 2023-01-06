from airflow import DAG, utils
from airflow.operators.bash import BashOperator


def helloDag() -> str:
    print('Hello, I ran successfully!')


dag = DAG('Demo', description='EL DAG',
          schedule_interval='* * * * *',
          start_date=utils.dates.days_ago(0), catchup=False)

hello = BashOperator(
    task_id='Dag_Test',
    bash_command='echo "Hello"',
    dag=dag)


hello

if __name__ == '__main__':
    dag.cli()
