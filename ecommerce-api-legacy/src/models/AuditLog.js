const { dbQuery } = require('../config/db');

class AuditLogModel {
    static async log(action) {
        return await dbQuery.run(
            "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
            [action]
        );
    }
}

module.exports = AuditLogModel;
