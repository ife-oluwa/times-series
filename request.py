import requests
import datetime as DT
import json
import psycopg2
from airflow import DAG
from airflow.operators.python_operators import PythonOperator


def getDates() -> list:
    dates = []
    for i in range(0, 8):
        date = (DT.datetime.today() - DT.timedelta(days=i)).strftime('%Y-%m-%d')
        dates.append(date)
    return dates


def extractData(dates: list) -> None:
    data_list = []
    for date in dates:
        year, month, day = date.split('-')
        URI = f'https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=Lille&lang=en&rows=100&sort=date&refine.date={year}%2F{month}%2F{day}'
        print(year, month, day)
        with requests.Session() as s:
            resp = requests.get(URI)

            resp = resp.json()
            for record in resp['records']:
                data_dict = dict()
                data_dict['date'] = record['fields'].get('date')
                data_dict['date_claimed'] = record['fields'].get(
                    'gc_obo_date_heure_restitution_c')
                data_dict['gare'] = record['fields'].get(
                    'gc_obo_gare_origine_r_name')
                data_dict['item_cat'] = record['fields'].get('gc_obo_type_c')
                data_dict['item'] = record['fields'].get('gc_obo_nature_c')
                data_dict['found/not_found'] = record['fields'].get(
                    'gc_obo_nom_recordtype_sc_c')
                data_list.append(data_dict)
    with open('test.json', 'w') as f:
        json.dump(data_list, f)


def loadData() -> None:
    conn_string = "host=localhost port=5432 dbname=sncf user=postgres password=docker"
    print("Connecting to db")
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    with open('test.json', 'r') as f:
        data = json.load(f)
    for record in data:
        date = record['date']
        date_claimed = record['date_claimed']
        gare = record['gare']
        item_cat = record['item_cat']
        item = record['item']
        found = record['found/not_found']
        cur.execute(
            "INSERT INTO public.sncf (date, return_date, gare, item_cat, item, found_not_found) VALUES (%s, %s, %s, %s, %s, %s)", (date, date_claimed, gare, item_cat, item, found))
        conn.commit()
    cur.execute('SELECT COUNT(*) FROM public.sncf;')
    print(cur.fetchone())
    conn.commit()
    cur.close()
    conn.close()


dag = DAG('EL', description='EL DAG',
          schedule_interval='0 10 * * 2',
          start_date=DT.datetime(2023, 1, 6), catchup=False)

dates = PythonOperator(task_id='Get dates', python_callable=getDates, dag=dag)

extract = PythonOperator(
    task_id='Get data', python_callable=extractData, dag=dag)

load = PythonOperator(task_id='Get data', python_callable=loadData, dag=dag)

dates >> extract >> load
