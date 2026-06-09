const { dbQuery } = require('../config/db');

class EnrollmentModel {
    static async create(userId, courseId) {
        const result = await dbQuery.run(
            "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
            [userId, courseId]
        );
        return result.lastID;
    }

    static async deleteByUser(userId) {
        return await dbQuery.run("DELETE FROM enrollments WHERE user_id = ?", [userId]);
    }
}

module.exports = EnrollmentModel;
