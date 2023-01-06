#! /home/ifeoluwa/anaconda3/bin/python
import requests
import datetime as DT
import json
import psycopg2


def getSncfData(days: str) -> dict:
    today = DT.date.today()
    data = dict()
    for i in range(1, days):
        date = str(today - DT.timedelta(days=i)).split('-')
        year, month, day = date
        url = f'https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=Lille&\
            lang=en&sort=gc_obo_type_c&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&\
            facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2023%2F{month}%2F{day}'
        resp = requests.get(url)


def extractData() -> None:

    data_list = []
    status_list = []
    for year in range(2016, 2024):
        url = f'https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=Lille&lang=en&rows=10000&refine.date={year}'
        with requests.Session() as s:
            resp = requests.get(url)

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
    with open('file.json', 'w') as f:
        json.dump(data_list, f)


def loadData() -> None:
    # with open('ps.json', 'r') as f:
    conn_string = "host=localhost port=5432 dbname=sncf user=postgres password=docker"
    print("Connecting to db")
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    query = """
            SELECT * FROM public.sncf
            """
    cur.execute(query)
    record = cur.fetchall()

    with open('file.json', 'r') as f:
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


loadData()
