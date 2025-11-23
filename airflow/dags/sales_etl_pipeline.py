from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2
from pymongo import MongoClient
import logging

default_args = {
    'owner': 'facebook_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

def extract_data():
    """Extrait les données de PostgreSQL"""
    try:
        logging.info("🔍 Début de l'extraction depuis PostgreSQL...")
        
        conn = psycopg2.connect(
            host="sales_postgres",
            database="sales_db",
            user="admin",
            password="password",
            port="5432"
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, product_name, quantity, price, sale_date, category, region, customer_id 
            FROM sales
        """)
        
        sales_data = []
        for row in cursor.fetchall():
            sales_data.append({
                'id': row[0],
                'product_name': row[1],
                'quantity': row[2],
                'price': float(row[3]),
                'sale_date': row[4].isoformat() if row[4] else None,
                'category': row[5],
                'region': row[6],
                'customer_id': row[7]
            })
        
        cursor.close()
        conn.close()
        
        logging.info(f"✅ {len(sales_data)} enregistrements extraits de PostgreSQL")
        return sales_data
        
    except Exception as e:
        logging.error(f"❌ Erreur extraction: {str(e)}")
        raise

def transform_data(**context):
    """Transforme les données extraites"""
    try:
        sales_data = context['task_instance'].xcom_pull(task_ids='extract_data')
        logging.info("🔄 Début de la transformation des données...")
        
        transformed_data = []
        for sale in sales_data:
            # Calcul du revenu total
            total_revenue = sale['quantity'] * sale['price']
            
            # Ajout de métriques calculées
            transformed_sale = {
                **sale,
                'total_revenue': total_revenue,
                'is_high_value': total_revenue > 1000,
                'revenue_category': 'High' if total_revenue > 1000 else 'Medium' if total_revenue > 500 else 'Low',
                'etl_processed_at': datetime.now().isoformat(),
                'year': datetime.strptime(sale['sale_date'], '%Y-%m-%d').year if sale['sale_date'] else None,
                'month': datetime.strptime(sale['sale_date'], '%Y-%m-%d').month if sale['sale_date'] else None
            }
            transformed_data.append(transformed_sale)
        
        logging.info(f"✅ {len(transformed_data)} enregistrements transformés")
        return transformed_data
        
    except Exception as e:
        logging.error(f"❌ Erreur transformation: {str(e)}")
        raise

def load_data(**context):
    """Charge les données transformées dans MongoDB"""
    try:
        transformed_data = context['task_instance'].xcom_pull(task_ids='transform_data')
        logging.info("📤 Début du chargement vers MongoDB...")
        
        client = MongoClient(
            'mongodb://admin:password@sales_mongodb:27017/',
            authSource='admin'
        )
        
        db = client['sales_analytics']
        collection = db['sales']
        
        # Nettoyer la collection avant de charger de nouvelles données
        collection.delete_many({})
        
        # Insérer les nouvelles données
        if transformed_data:
            result = collection.insert_many(transformed_data)
            logging.info(f"✅ {len(result.inserted_ids)} enregistrements chargés dans MongoDB")
        else:
            logging.warning("⚠️ Aucune donnée à charger")
        
        client.close()
        
        # Statistiques
        stats = {
            'total_records': len(transformed_data),
            'total_revenue': sum(sale['total_revenue'] for sale in transformed_data),
            'avg_revenue_per_sale': sum(sale['total_revenue'] for sale in transformed_data) / len(transformed_data),
            'high_value_sales': len([s for s in transformed_data if s['is_high_value']])
        }
        
        logging.info(f"📊 Statistiques finales: {stats}")
        return stats
        
    except Exception as e:
        logging.error(f"❌ Erreur chargement: {str(e)}")
        raise

# Définition du DAG
with DAG(
    'sales_etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline for Sales Data from PostgreSQL to MongoDB',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=['sales', 'etl', 'facebook_engineer']
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )
    
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )
    
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )
    
    extract_task >> transform_task >> load_task
