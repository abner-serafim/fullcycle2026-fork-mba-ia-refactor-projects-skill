const FinancialService = require('../services/FinancialService');

class AdminController {
    static async getFinancialReport(req, res) {
        try {
            const report = await FinancialService.getFinancialReport();
            return res.json(report);
        } catch (err) {
            return res.status(500).send("Erro DB");
        }
    }
}

module.exports = AdminController;
