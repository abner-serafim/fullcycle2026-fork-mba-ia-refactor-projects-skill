const UserService = require('../services/UserService');

class UserController {
    static async deleteUser(req, res) {
        const id = req.params.id;
        try {
            await UserService.deleteUser(id);
            return res.send("Usuário deletado com sucesso, limpando também suas matrículas e pagamentos associados.");
        } catch (err) {
            return res.status(500).send("Erro ao deletar usuário");
        }
    }
}

module.exports = UserController;
