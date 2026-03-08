import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import './index.css';

const socket = io('http://localhost:3001');

const projects = [
  {
    id: 'product-spin',
    icon: '💎',
    title: 'Comercial 360',
    desc: 'Iluminação de estúdio hiper-realista para apresentação rotativa de produtos e joias.',
    accent: '#FFD700'
  },
  {
    id: 'liquid-splash',
    icon: '🌊',
    title: 'Liquid Splash',
    desc: 'Simulação MantaFlow para bebidas em câmera super lenta com refração precisa.',
    accent: '#00F0FF'
  },
  {
    id: 'samurai-fight',
    icon: '⚔️',
    title: 'Duelo Samurai',
    desc: 'Animação MocAp com espadas colidindo, sparks de partículas e DoF cinemático.',
    accent: '#FF3366'
  },
  {
    id: 'f1-tunnel',
    icon: '🏎️',
    title: 'F1 em Túnel',
    desc: 'Corrida de alta velocidade fazendo transição de pista para túnel iluminado a neon.',
    accent: '#00FF66'
  },
  {
    id: 'micro-landscape',
    icon: '⛰️',
    title: 'Macro Landscape',
    desc: 'Mundo miniatura hiperdetalhado revelado através de lentes macro extremas.',
    accent: '#FFA500'
  }
];

function App() {
  const [renders, setRenders] = useState<Record<string, { percent: number, status: string }>>({});

  useEffect(() => {
    socket.on('render-progress', (data) => {
      setRenders(prev => ({
        ...prev,
        [data.projectId]: { percent: data.percent, status: 'Gerando Frames...' }
      }));
    });

    socket.on('render-finished', (data) => {
      setRenders(prev => ({
        ...prev,
        [data.projectId]: { percent: 100, status: data.success ? 'Finalizado! ✅' : 'Erro ❌' }
      }));
    });

    return () => {
      socket.off('render-progress');
      socket.off('render-finished');
    };
  }, []);

  const handleLaunch = async (projectId: string) => {
    if (renders[projectId] && (renders[projectId].percent > 0 && renders[projectId].percent < 100)) {
      alert('Este render já está em andamento!');
      return;
    }

    try {
      setRenders(prev => ({
        ...prev,
        [projectId]: { percent: 0, status: 'Iniciando Blender...' }
      }));

      await fetch('http://localhost:3001/api/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectId })
      });
    } catch (err) {
      alert('Erro ao conectar com o Broker FGS.');
    }
  };

  return (
    <>
      <div className="mesh-bg"></div>

      <div className="dashboard-container">
        <header className="hero">
          <h1>FGS Studio</h1>
          <p>Motor de Produção 3D Autônomo. Escolha o cenário para o Blender gerar o reality code.</p>
        </header>

        <div className="project-grid">
          {projects.map((project) => (
            <div
              key={project.id}
              className="glass-card"
              style={{ '--custom-accent': project.accent } as React.CSSProperties}
            >
              <div
                className="card-icon"
                style={{ background: `linear-gradient(135deg, ${project.accent}, #ffffff)`, WebkitBackgroundClip: 'text', backgroundClip: 'text', WebkitTextFillColor: 'transparent' }}
              >
                {project.icon}
              </div>
              <h3 className="card-title">{project.title}</h3>
              <p className="card-desc">{project.desc}</p>

              {renders[project.id] && (
                <div className="progress-section">
                  <div className="progress-container">
                    <div
                      className="progress-bar"
                      style={{ width: `${renders[project.id].percent}%`, background: `linear-gradient(90deg, ${project.accent}, #ffffff)` }}
                    ></div>
                  </div>
                  <p className="progress-text" style={{ color: project.accent }}>
                    {renders[project.id].status} {renders[project.id].percent}%
                  </p>
                </div>
              )}

              <button
                className="btn-launch"
                onClick={() => handleLaunch(project.id)}
                disabled={renders[project.id]?.percent > 0 && renders[project.id]?.percent < 100}
                style={{ marginTop: renders[project.id] ? '1rem' : 'auto' }}
              >
                <span>{renders[project.id]?.percent > 0 && renders[project.id]?.percent < 100 ? 'Processando...' : 'Configurar & Renderizar'}</span>
                <span>→</span>
              </button>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default App;
