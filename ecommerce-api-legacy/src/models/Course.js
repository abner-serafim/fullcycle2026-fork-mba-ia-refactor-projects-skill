const { dbQuery } = require('../config/db');

class CourseModel {
    static async findActiveById(id) {
        return await dbQuery.get("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
    }

    static async findAll() {
        return await dbQuery.all("SELECT * FROM courses");
    }
}

module.exports = CourseModel;
