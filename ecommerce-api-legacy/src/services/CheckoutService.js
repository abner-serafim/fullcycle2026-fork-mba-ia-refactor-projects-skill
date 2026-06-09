const UserModel = require('../models/User');
const CourseModel = require('../models/Course');
const EnrollmentModel = require('../models/Enrollment');
const PaymentModel = require('../models/Payment');
const AuditLogModel = require('../models/AuditLog');
const AuthService = require('./AuthService');
const env = require('../config/env');
const { logAndCache } = require('../utils');

class CheckoutService {
    static async processCheckout({ username, email, password, courseId, cardNumber }) {
        const course = await CourseModel.findActiveById(courseId);
        if (!course) {
            const err = new Error("Curso não encontrado");
            err.statusCode = 404;
            throw err;
        }

        let user = await UserModel.findByEmail(email);
        let userId;

        if (!user) {
            const passwordHash = AuthService.hashPassword(password || "123456");
            userId = await UserModel.create(username, email, passwordHash);
        } else {
            userId = user.id;
        }

        console.log(`Processando cartão ${cardNumber} na chave ${env.paymentGatewayKey}`);
        const status = cardNumber.startsWith("4") ? "PAID" : "DENIED";

        if (status === "DENIED") {
            const err = new Error("Pagamento recusado");
            err.statusCode = 400;
            throw err;
        }

        const enrollmentId = await EnrollmentModel.create(userId, courseId);
        await PaymentModel.create(enrollmentId, course.price, status);
        await AuditLogModel.log(`Checkout curso ${courseId} por ${userId}`);

        logAndCache(`last_checkout_${userId}`, course.title);

        return { enrollmentId };
    }
}

module.exports = CheckoutService;
