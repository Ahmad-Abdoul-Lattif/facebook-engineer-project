# 📊 Projet Facebook Engineer - Application RESTful avec ETL

## 🎯 Description du Projet
Application RESTful complète développée avec Express.js utilisant un pipeline ETL pour transférer les données de ventes de PostgreSQL vers MongoDB, avec monitoring Grafana et Prometheus.

## 🏗️ Architecture
PostgreSQL → ETL Pipeline → MongoDB → API Express.js → Grafana + Prometheus


## ✅ Fonctionnalités Implémentées

### 🔄 Pipeline ETL
- **Extraction** : 12 ventes depuis PostgreSQL
- **Transformation** : Calcul du revenue total, catégorisation, métriques avancées
- **Chargement** : Vers MongoDB avec nettoyage et statistiques
- **Résultat** : 12,299.71 € de revenue total transféré

### 🌐 API RESTful (Express.js)
- `GET /api/health` ✅ - Statut de l'API
- `GET /api/sales` ✅ - Liste toutes les ventes avec pagination et filtres
- `GET /api/sales/:id` ✅ - Vente spécifique
- `GET /api/sales/stats` ✅ - Statistiques globales
- `POST /api/sales` ✅ - Créer une nouvelle vente

### 📊 Monitoring (Grafana + Prometheus)
- Dashboard de monitoring système
- Métriques CPU, mémoire, disque, réseau en temps réel
- Analyse des performances de l'infrastructure

## 🚀 Installation et Démarrage

### Prérequis
- Docker et Docker Compose
- Node.js 18+
- Python 3.8+

### 1. Cloner le projet
```bash
git clone https://github.com/Ahmad-Abdoul-Lattif/facebook-engineer-project.git
cd facebook-engineer-project

### 2. Démarrage de l'infrastructure
sudo docker-compose -f docker-compose-simple.yml up -d

# Vérification des données PostgreSQL
sudo docker exec sales_postgres psql -U admin -d sales_db -c "SELECT COUNT(*) FROM sales;"

# Exécution du pipeline ETL
python3 etl_standalone.py

### Démarrage de l'API
cd api
npm install
npm run dev

### 5. Accès aux interfaces

    Grafana : http://localhost:3000 (admin/admin)

    Prometheus : http://localhost:9090

    API Documentation : http://localhost:3001/api/health

###Test du pipeline ETL
python3 etl_standalone.py

###Test de l'API RESTful

# Santé de l'API
curl http://localhost:3001/api/health

# Liste des ventes (premières 10)
curl http://localhost:3001/api/sales

# Statistiques détaillées
curl http://localhost:3001/api/sales/stats

# Vente spécifique
curl http://localhost:3001/api/sales/1

facebook-engineer-project/
├── 📁 api/                          # Application Express.js complète
│   ├── 📁 models/                   # Modèles MongoDB
│   │   └── Sale.js
│   ├── 📁 routes/                   # Routes API
│   │   └── sales.js
│   ├── 📁 controllers/              # Contrôleurs
│   │   └── saleController.js
│   ├── app.js                       # Application principale
│   ├── server.js                    # Serveur Node.js
│   └── package.json
├── 📁 scripts/
│   └── init_postgresql.sql          # Données de test PostgreSQL (12 ventes)
├── 📁 airflow/dags/                 # DAGs Airflow
│   └── sales_etl_pipeline.py
├── docker-compose-simple.yml        # Infrastructure Docker simplifiée
├── docker-compose.yml               # Infrastructure Docker complète
├── prometheus.yml                   # Configuration Prometheus
├── promtail-config.yml              # Configuration Promtail (logs)
├── etl_standalone.py               # Script ETL Python autonome
├── etl_corrected.py                # Script ETL corrigé
└── README.md
