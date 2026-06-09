const express = require('express');
const initDb = require('./config/dbInit');
const routes = require('./routes');
const env = require('./config/env');

const app = express();
app.use(express.json());

initDb().then(() => {
    app.use('/api', routes);

    app.listen(env.port, () => {
        console.log(`Frankenstein LMS rodando na porta ${env.port}...`);
    });
}).catch(err => {
    console.error("Failed to initialize database:", err);
    process.exit(1);
});
