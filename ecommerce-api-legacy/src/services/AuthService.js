const bcrypt = require('bcryptjs');

class AuthService {
    static hashPassword(password) {
        return bcrypt.hashSync(password, 10);
    }

    static comparePassword(password, hash) {
        return bcrypt.compareSync(password, hash);
    }
}

module.exports = AuthService;
