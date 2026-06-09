const express = require('express');
const CheckoutController = require('../controllers/CheckoutController');
const AdminController = require('../controllers/AdminController');
const UserController = require('../controllers/UserController');

const router = express.Router();

router.post('/checkout', CheckoutController.checkout);
router.get('/admin/financial-report', AdminController.getFinancialReport);
router.delete('/users/:id', UserController.deleteUser);

module.exports = router;
