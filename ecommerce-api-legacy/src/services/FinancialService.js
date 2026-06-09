const { dbQuery } = require('../config/db');

class FinancialService {
    static async getFinancialReport() {
        const rows = await dbQuery.all(`
            SELECT 
                c.id AS course_id,
                c.title AS course_title,
                u.name AS student_name,
                p.amount AS payment_amount,
                p.status AS payment_status
            FROM courses c
            LEFT JOIN enrollments e ON e.course_id = c.id
            LEFT JOIN users u ON u.id = e.user_id
            LEFT JOIN payments p ON p.enrollment_id = e.id
        `);

        const coursesMap = {};

        for (const row of rows) {
            if (!coursesMap[row.course_id]) {
                coursesMap[row.course_id] = {
                    course: row.course_title,
                    revenue: 0,
                    students: []
                };
            }

            if (row.student_name !== null) {
                const isPaid = row.payment_status === 'PAID';
                const paidAmount = row.payment_amount || 0;
                
                if (isPaid) {
                    coursesMap[row.course_id].revenue += paidAmount;
                }

                coursesMap[row.course_id].students.push({
                    student: row.student_name || 'Unknown',
                    paid: paidAmount
                });
            }
        }

        return Object.values(coursesMap);
    }
}

module.exports = FinancialService;
