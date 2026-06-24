const env = require('./config/env');

const config = {
    dbUser: env.dbUser,
    dbPass: env.dbPass,
    paymentGatewayKey: env.paymentGatewayKey,
    smtpUser: env.smtpUser,
    port: env.port
};

let globalCache = {};
let totalRevenue = 0;

const MAX_CACHE_SIZE = 100;

function logAndCache(key, data) {
    console.log(`[LOG] Salvando no cache: ${key}`);
    
    // Prevenção de Memory Leak: política de expiração básica (evicção por tamanho máximo)
    const keys = Object.keys(globalCache);
    if (keys.length >= MAX_CACHE_SIZE) {
        const oldestKey = keys[0];
        delete globalCache[oldestKey];
    }
    
    globalCache[key] = data;
}

module.exports = { config, logAndCache, globalCache, totalRevenue };
