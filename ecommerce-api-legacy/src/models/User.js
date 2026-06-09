const { dbQuery } = require('../config/db');

class UserModel {
    static async create(name, email, passwordHash) {
        const result = await dbQuery.run(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            [name, email, passwordHash]
        );
        return result.lastID;
    }

    static async findByEmail(email) {
        return await dbQuery.get("SELECT * FROM users WHERE email = ?", [email]);
    }

    static async findById(id) {
        return await dbQuery.get("SELECT name, email FROM users WHERE id = ?", [id]);
    }

    static async delete(id) {
        return await dbQuery.run("DELETE FROM users WHERE id = ?", [id]);
    }
}

module.exports = UserModel;
