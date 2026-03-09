const http = require('http');

const data = JSON.stringify({
    projectId: 'nike-auto-v2'
});

const options = {
    hostname: 'localhost',
    port: 3001,
    path: '/api/render',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }
};

console.log("🚀 FGS Studio: Enviando solicitação de renderização para o Broker...");

const req = http.request(options, (res) => {
    let responseData = '';

    res.on('data', (chunk) => {
        responseData += chunk;
    });

    res.on('end', () => {
        console.log(`✅ Status: ${res.statusCode}`);
        console.log(`📩 Resposta: ${responseData}`);
    });
});

req.on('error', (error) => {
    console.error(`❌ Erro: Certifique-se de que o Broker (server.js) está rodando!`);
    console.error(error.message);
});

req.write(data);
req.end();
