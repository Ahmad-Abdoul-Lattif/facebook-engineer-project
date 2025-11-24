const Sale = require('../models/Sale');

// GET all sales
const getAllSales = async (req, res) => {
    try {
        const { page = 1, limit = 10, category, region } = req.query;
        
        let filter = {};
        if (category) filter.category = category;
        if (region) filter.region = region;
        
        const sales = await Sale.find(filter)
            .limit(limit * 1)
            .skip((page - 1) * limit)
            .sort({ sale_date: -1 });
        
        const total = await Sale.countDocuments(filter);
        
        res.json({
            success: true,
            data: sales,
            pagination: {
                currentPage: parseInt(page),
                totalPages: Math.ceil(total / limit),
                totalItems: total,
                itemsPerPage: parseInt(limit)
            }
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

// GET sale by ID
const getSaleById = async (req, res) => {
    try {
        const sale = await Sale.findOne({ id: parseInt(req.params.id) });
        if (!sale) {
            return res.status(404).json({ success: false, error: 'Sale not found' });
        }
        res.json({ success: true, data: sale });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

// GET sales statistics
const getSalesStats = async (req, res) => {
    try {
        const stats = await Sale.aggregate([
            {
                $group: {
                    _id: null,
                    totalRevenue: { $sum: "$total_revenue" },
                    totalSales: { $sum: 1 },
                    averageRevenue: { $avg: "$total_revenue" },
                    maxRevenue: { $max: "$total_revenue" },
                    minRevenue: { $min: "$total_revenue" }
                }
            }
        ]);
        
        const categoryStats = await Sale.aggregate([
            {
                $group: {
                    _id: "$category",
                    totalRevenue: { $sum: "$total_revenue" },
                    totalSales: { $sum: 1 }
                }
            }
        ]);
        
        res.json({
            success: true,
            data: {
                overall: stats[0] || {},
                byCategory: categoryStats
            }
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

// CREATE new sale
// CREATE new sale - AVEC ID AUTOMATIQUE
const createSale = async (req, res) => {
    try {
        const saleData = req.body;
        
        // Vérification des champs obligatoires
        if (!saleData.product_name || !saleData.quantity || !saleData.price) {
            return res.status(400).json({
                success: false,
                error: 'product_name, quantity et price sont obligatoires'
            });
        }
        
        // Trouver le PLUS GRAND ID existant et ajouter 1
        const lastSale = await Sale.findOne().sort({ id: -1 });
        const nextId = lastSale ? lastSale.id + 1 : 1000; // Commence à 1000 pour les ajouts API
        
        // Conversion des types
        const quantity = Number(saleData.quantity);
        const price = Number(saleData.price);
        
        if (isNaN(quantity) || isNaN(price)) {
            return res.status(400).json({
                success: false,
                error: 'quantity et price doivent être des nombres valides'
            });
        }
        
        // Calculs automatiques
        const total_revenue = quantity * price;
        const is_high_value = total_revenue > 1000;
        const revenue_category = total_revenue > 1000 ? 'High' : 
                               total_revenue > 500 ? 'Medium' : 'Low';
        
        const finalSaleData = {
            id: nextId, // ← ID AUTOMATIQUE !
            product_name: saleData.product_name,
            quantity: quantity,
            price: price,
            sale_date: saleData.sale_date || new Date().toISOString().split('T')[0],
            category: saleData.category || 'General',
            region: saleData.region || 'Unknown',
            customer_id: Number(saleData.customer_id) || 1000,
            total_revenue: total_revenue,
            is_high_value: is_high_value,
            revenue_category: revenue_category,
            etl_processed_at: new Date().toISOString()
        };
        
        const sale = new Sale(finalSaleData);
        await sale.save();
        
        res.status(201).json({
            success: true,
            message: 'Vente créée avec succès',
            data: sale
        });
        
    } catch (error) {
        console.error('Erreur création vente:', error);
        res.status(400).json({
            success: false,
            error: error.message
        });
    }
};

module.exports = {
    getAllSales,
    getSaleById,
    getSalesStats,
    createSale
};
