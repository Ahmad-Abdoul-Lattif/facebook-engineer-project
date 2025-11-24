import psycopg2
from pymongo import MongoClient
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_etl_pipeline():
    try:
        # EXTRACTION - Connexion au service PostgreSQL Docker
        logger.info('🔍 Extraction des données depuis PostgreSQL...')
        conn = psycopg2.connect(
            host='sales_postgres',  # Nom du service Docker
            database='sales_db',
            user='admin',
            password='password',
            port='5432'
        )
        
        cursor = conn.cursor()
        cursor.execute('SELECT id, product_name, quantity, price, sale_date, category, region, customer_id FROM sales')
        
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
        logger.info(f'✅ {len(sales_data)} enregistrements extraits')
        
        # TRANSFORMATION
        logger.info('🔄 Transformation des données...')
        transformed_data = []
        for sale in sales_data:
            total_revenue = sale['quantity'] * sale['price']
            transformed_sale = {
                **sale,
                'total_revenue': total_revenue,
                'is_high_value': total_revenue > 1000,
                'revenue_category': 'High' if total_revenue > 1000 else 'Medium' if total_revenue > 500 else 'Low',
                'etl_processed_at': datetime.now().isoformat()
            }
            transformed_data.append(transformed_sale)
        
        logger.info(f'✅ {len(transformed_data)} enregistrements transformés')
        
        # CHARGEMENT - Connexion au service MongoDB Docker
        logger.info('📤 Chargement vers MongoDB...')
        client = MongoClient(
            'mongodb://admin:password@sales_mongodb:27017/',  # Nom du service Docker
            authSource='admin'
        )

        db = client['sales_analytics']
        collection = db['sales']

        # ⚡ AMÉLIORATION : Sauvegarder les ventes API (IDs >= 1000)
        api_sales = list(collection.find({"id": {"$gte": 1000}}))
        logger.info(f'💾 {len(api_sales)} ventes API sauvegardées')

        # Nettoyer seulement les ventes PostgreSQL (IDs 1-999)
        collection.delete_many({"id": {"$lt": 1000}})

        if transformed_data:
            result = collection.insert_many(transformed_data)
            logger.info(f'✅ {len(result.inserted_ids)} ventes PostgreSQL chargées')

        # Statistiques finales
        total_count = collection.count_documents({})
        postgres_count = collection.count_documents({"id": {"$lt": 1000}})
        api_count = collection.count_documents({"id": {"$gte": 1000}})

        stats = {
            'total_records': total_count,
            'postgres_sales': postgres_count,
            'api_sales': api_count,
            'total_revenue': sum(sale['total_revenue'] for sale in transformed_data)
        }

        logger.info(f'📊 Statistiques: {stats}')
        client.close()

        print(f'🎉 ETL AMÉLIORÉ TERMINÉ!')
        print(f'📈 {postgres_count} ventes PostgreSQL + {api_count} ventes API')
        print(f'💰 Revenue total: {stats["total_revenue"]:.2f} €')
        return True
        
    except Exception as e:
        logger.error(f'❌ Erreur ETL: {str(e)}')
        return False

if __name__ == "__main__":
    run_etl_pipeline()