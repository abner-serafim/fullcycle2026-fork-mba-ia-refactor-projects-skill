const UserModel = require('../models/User');
const EnrollmentModel = require('../models/Enrollment');
const PaymentModel = require('../models/Payment');

class UserService {
    static async deleteUser(id) {
        await PaymentModel.deleteByUser(id);
        await EnrollmentModel.deleteByUser(id);
        await UserModel.delete(id);
    }
}

module.exports = UserService;
