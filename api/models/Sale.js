const mongoose = require('mongoose');

const saleSchema = new mongoose.Schema({
    id: { type: Number, required: true },
    product_name: { type: String, required: true },
    quantity: { type: Number, required: true },
    price: { type: Number, required: true },
    sale_date: { type: String, required: true },
    category: { type: String, required: true },
    region: { type: String, required: true },
    customer_id: { type: Number, required: true },
    total_revenue: { type: Number, required: true },
    is_high_value: { type: Boolean, required: true },
    revenue_category: { type: String, required: true },
    etl_processed_at: { type: String, required: true }
}, {
    timestamps: true
});

module.exports = mongoose.model('Sale', saleSchema);
