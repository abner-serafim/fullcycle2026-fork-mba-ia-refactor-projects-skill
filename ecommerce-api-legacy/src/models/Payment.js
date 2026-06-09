const { dbQuery } = require('../config/db');

class PaymentModel {
    static async create(enrollmentId, amount, status) {
        const result = await dbQuery.run(
            "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
            [enrollmentId, amount, status]
        );
        return result.lastID;
    }

    static async deleteByUser(userId) {
        return await dbQuery.run(
            "DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)",
            [userId]
        );
    }
}

module.exports = PaymentModel;
