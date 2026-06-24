const CheckoutService = require('../services/CheckoutService');

class CheckoutController {
    static async checkout(req, res) {
        const { usr, eml, pwd, c_id, card } = req.body;

        if (!usr || !eml || !c_id || !card) {
            return res.status(400).send("Bad Request");
        }

        try {
            const result = await CheckoutService.processCheckout({
                username: usr,
                email: eml,
                password: pwd,
                courseId: c_id,
                cardNumber: card
            });
            return res.status(200).json({ msg: "Sucesso", enrollment_id: result.enrollmentId });
        } catch (err) {
            const statusCode = err.statusCode || 500;
            const message = statusCode === 500 ? "Erro interno no servidor" : err.message;
            return res.status(statusCode).send(message);
        }
    }
}

module.exports = CheckoutController;
