const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "http://localhost:5173",
        methods: ["GET", "POST"]
    }
});

const port = 3001;

app.use(cors());
app.use(express.json());

const blenderPath = path.join(__dirname, '..', 'tools', 'blender', 'blender.exe');
const scriptsDir = path.join(__dirname, '..', 'scripts');

const projectScripts = {
    'product-spin': 'commercials/product_spin_360.py',
    'liquid-splash': 'commercials/liquid_splash.py',
    'samurai-fight': 'youtube/samurai_fight.py',
    'f1-tunnel': 'commercials/f1_tunnel.py',
    'micro-landscape': 'scenes/micro_landscape.py'
};

app.post('/api/render', (req, res) => {
    const { projectId } = req.body;
    const scriptSubPath = projectScripts[projectId];

    if (!scriptSubPath) return res.status(400).json({ error: 'Projeto não encontrado' });

    const scriptPath = path.join(scriptsDir, scriptSubPath);
    if (!fs.existsSync(scriptPath)) {
        return res.status(404).json({ error: 'Script não encontrado' });
    }

    // Usamos spawn em vez de exec para ler o fluxo de saída em tempo real
    const blender = spawn(blenderPath, ['-b', '-P', scriptPath]);

    blender.stdout.on('data', (data) => {
        const output = data.toString();
        console.log(output);

        // Regex para capturar frames de diferentes versões/saídas
        const frameMatch = output.match(/Append frame (\d+)/) ||
            output.match(/Fra:(\d+)/) ||
            output.match(/Frame:(\d+)/) ||
            output.match(/(\d+)\/150/); // Fallback para progress customizado

        if (frameMatch) {
            const currentFrame = parseInt(frameMatch[1]);
            // Tentamos detectar o frame final do output ou usamos 150 como base segura
            const totalFrames = projectId === 'f1-tunnel' ? 250 : 150;
            const percent = Math.min(Math.round((currentFrame / totalFrames) * 100), 100);
            io.emit('render-progress', { projectId, currentFrame, percent });
        }
    });

    blender.on('close', (code) => {
        io.emit('render-finished', { projectId, success: code === 0 });
    });

    res.json({ message: 'Render iniciado com monitoramento via WebSocket.' });
});

server.listen(port, () => {
    console.log(`🤖 Broker Real-time rodando em http://localhost:${port}`);
});
