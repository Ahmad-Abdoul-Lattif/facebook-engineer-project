const express = require('express');
const router = express.Router();
const {
    getAllSales,
    getSaleById,
    getSalesStats,
    createSale
} = require('../controllers/saleController');

// GET /api/sales - Get all sales with filtering
router.get('/', getAllSales);

// GET /api/sales/stats - Get sales statistics
router.get('/stats', getSalesStats);

// GET /api/sales/:id - Get single sale
router.get('/:id', getSaleById);

// POST /api/sales - Create new sale
router.post('/', createSale);

module.exports = router;
