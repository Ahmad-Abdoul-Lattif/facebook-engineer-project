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
const createSale = async (req, res) => {
    try {
        const saleData = req.body;
        saleData.total_revenue = saleData.quantity * saleData.price;
        saleData.is_high_value = saleData.total_revenue > 1000;
        saleData.revenue_category = saleData.total_revenue > 1000 ? 'High' : 
                                   saleData.total_revenue > 500 ? 'Medium' : 'Low';
        saleData.etl_processed_at = new Date().toISOString();
        
        const sale = new Sale(saleData);
        await sale.save();
        
        res.status(201).json({ success: true, data: sale });
    } catch (error) {
        res.status(400).json({ success: false, error: error.message });
    }
};

module.exports = {
    getAllSales,
    getSaleById,
    getSalesStats,
    createSale
};
