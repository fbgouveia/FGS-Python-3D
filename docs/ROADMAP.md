# ROADMAP — BLENDERSCRIPTS
**Felipe Gouveia Studio | EUvc Pipeline**
**Base: 2026-03-15 | Revisão: mensal**

---

## VISÃO GERAL

```
HOJE         → Pipeline funcional localmente
MÊS 1        → Sistema estável, primeiro cliente real
MÊS 2        → Templates por nicho validados
MÊS 3        → Produto white-label empacotado
MÊS 4+       → SaaS / API / Lançamento comercial
```

---

## FASE 1 — ESTABILIZAÇÃO (Semanas 1-2)
**Objetivo: Pipeline JSON → Blender → render rodando sem erros**

| # | Tarefa | Status |
|---|--------|--------|
| 1.1 | bridge_engine.py: métodos corretos | ✅ FEITO |
| 1.2 | paths.py: GDR 477GB conectado | ✅ FEITO |
| 1.3 | lighting_system: load_hdri() | ✅ FEITO |
| 1.4 | audio_manager: from_library() | ✅ FEITO |
| 1.5 | FGS_PRODUCER_CORE.py: corrigir imports | ⏳ |
| 1.6 | Testar pipeline completo end-to-end | ⏳ |
| 1.7 | portfolio_builder: remover hardcode | ⏳ |
| 1.8 | lorena_system_guardian: inicializar DB | ⏳ |

**Entregável: `blender -b -P FGS_PRODUCER_CORE.py` roda sem erros**

---

## FASE 2 — INTELIGÊNCIA DE ASSETS (Semanas 3-4)
**Objetivo: dado um conceito, o sistema escolhe os assets sozinho**

| # | Tarefa | Status |
|---|--------|--------|
| 2.1 | Criar AssetSelector: conceito → mapa de assets | ⏳ |
| 2.2 | Conectar suggestion_engine → portfolio_builder → bridge_engine | ⏳ |
| 2.3 | VFX packs GDR conectados ao vfx_engine | ⏳ |
| 2.4 | LUTs GDR conectados ao render_manager | ⏳ |
| 2.5 | Instalar dependências: watchdog, gdown, duckduckgo-search | ⏳ |
| 2.6 | Configurar rclone: D:\GDR → Google Drive | ⏳ |

**Entregável: `criar_broll("ansiedade")` seleciona HDRI + música + LUT automaticamente**

---

## FASE 3 — TEMPLATES POR NICHO (Mês 2)
**Objetivo: 10+ templates prontos cobrindo os nichos principais**

| Template | Nicho | Status |
|----------|-------|--------|
| product_spin_360 | Produto premium | ✅ |
| broll_generator | Psicologia/Educação | ✅ |
| boomer_kev_ep01 | Podcast entretenimento | ✅ |
| liquid_splash | Gastronomia/Bebidas | ✅ |
| medical_journey | Medicina/Saúde | ✅ |
| logo_reveal | Branding/Corporativo | ✅ |
| particle_burst | Viral/Redes sociais | ✅ |
| news_explainer | Notícias/Educação | ⏳ |
| music_visualizer | Música/Entretenimento | ⏳ |
| architecture_flythrough | Imóveis/Construção | ⏳ |

**Entregável: 10 templates funcionando, 1 projeto piloto por nicho renderizado**

---

## FASE 4 — PRIMEIRO CLIENTE REAL (Final Mês 2)
**Objetivo: entregar um projeto pago usando o pipeline**

| Etapa | Descrição |
|-------|-----------|
| Prospecção | 300k+ psicólogos brasileiros — via Clara |
| Proposta | R$150-300/vídeo (B-roll conceitual 3D) |
| Entrega | broll_generator.py → render → portfolio_watcher → cliente |
| Feedback | Ajustar templates com base na entrega real |

**Entregável: 1 cliente pago, 1 vídeo entregue, pipeline validado comercialmente**

---

## FASE 5 — WHITE LABEL (Mês 3-4)
**Objetivo: empacotar o sistema para venda como produto**

| # | Item |
|---|------|
| 5.1 | Interface web de geração (formulário → script Python) |
| 5.2 | API REST: briefing → render |
| 5.3 | Dashboard de projetos e clientes |
| 5.4 | Sistema de licenças real (não mock) |
| 5.5 | Render em nuvem (GPU cloud) |
| 5.6 | Integração social: TikTok API, Instagram API, YouTube API |

**Entregável: produto vendável com painel de cliente + API**

---

## MARCOS CRÍTICOS

| Data estimada | Marco |
|---------------|-------|
| 2026-03-29 | Pipeline end-to-end funcionando sem erros |
| 2026-04-12 | AssetSelector operacional — assets automáticos |
| 2026-04-30 | 10 templates validados |
| 2026-05-15 | Primeiro cliente pago |
| 2026-06-30 | Produto white-label empacotado |

---

## DEPENDÊNCIAS EXTERNAS PENDENTES

| Ferramenta | Uso | Status |
|------------|-----|--------|
| ElevenLabs API Key | Geração de voz | ⏳ Felipe configura |
| Rhubarb Lip Sync | Lip sync automático | ⏳ Felipe instala |
| rclone + Google Drive | Mirror GDR 477GB | ⏳ Felipe configura |
| Windows Terminal | Fundo vinho no terminal | ⏳ `winget install Microsoft.WindowsTerminal` |

---

*EUvc — Felipe Gouveia Studio | Revisado a cada sessão*
