# 📘 CHARACTER SYSTEM – Felipe Gouveia Studio  
**Versão:** 2.0.0  
**Status:** IMPLEMENTATION – PRONTO PARA PRODUÇÃO  
**Autor:** @nvidia (Imperial Engineering)  

> *Este documento descreve a arquitetura, os fluxos de trabalho e os atalhos que compõem o sistema de personagens do estúdio. Ele serve como referência única para todos os agentes de criação.*

---

## 1. Visão Geral  

| Elemento | Descrição | Escopo |
|----------|-----------|--------|
| **Identity Presets** | Conjuntos predefinidos de proporções, cores, materiais e animações que garantem coerência premium. | Global – todos os personagens. |
| **Character Factory** | Classe centralizada (`CharacterFactory`) responsável por instanciar qualquer personagem via parâmetros ou presets. | Python (`scripts/utils/character_factory.py`). |
| **Presets Library** | Biblioteca de presets (`IdentityPresets`) contendo `MAESTRE_HERO`, `SUPPORT_AGENT`, `BACKGROUND_CREATURE`. | `scripts/utils/presets.py`. |
| **Animation Toolkit** | Conjunto de operadores de animação (Head-Bob, Inclinação, Risada, etc.). | `scripts/utils/animation.py`. |

---

## 2. Arquitetura de código  

```
d:\Blender\blenderscripts\  
│  
├─ characters\                # Personagens estáticos e presets  
│  
├─ scripts\  
│   ├─ utils\                 # Utilitários genéricos  
│   │   ├─ character_factory.py   # Fábrica universal  
│   │   ├─ animation.py        # Operadores de animação  
│   │   ├─ material_library.py # Biblioteca de materiais premium  
│   │  
│   └─ commercials\           # Scripts de produção prontos ao usuário  
│       └─ fgs_vibe_check.py  # POC de Identidade Visual  
│  
└─ docs\                      # Documentação  
```

### 2.1. `character_factory.py`  

- **Classe principal:** `CharacterFactory`  
  - `criar_preset(name)` – instancia um preset completo a partir da `IdentityPresets`.  
  - `criar_master_hero()` – shortcut para o benchmark de luxo.

---

## 3. Presets & Premium Standards  

| Preset | Descrição | Uso Principal |
|--------|-----------|----------------|
| `MAESTRE_HERO` | Personagem de referência "imperial". Pele dourada, olhos vivos, rig completo. | Campanhas premium, trailers. |
| `SUPPORT_AGENT` | Variantes de apoio. Menor detalhamento. | Cenas de fundo, secundários. |

---

## 4. Shortcuts de Produção (Roadmap)
- `factory.criar_preset('MAESTRE_HERO')` → Cria o hero em 1 clique.
- `hero.head_bob()` → Animação de fala.
- `hero.risada()` → Gatilho de humor.

---

## 5. Pipeline de Criação – Fluxo Imperial  

1. **Seleção de Preset** – Escolha do perfil (ex.: `MAESTRE_HERO`).  
2. **Instanciação** – `CharacterFactory` gera malhas, armature e materiais.  
3. **Animação** – Aplicação de comportamentos (head-bob, risada).  
4. **Iluminação** – Setup de 3 pontos cinematográfico.  
5. **Render** – Output otimizado em `renders/finals/`.

---

*Este documento é propriedade exclusiva do **Felipe Gouveia Studio**.*  
*Assinado: Imperial Documentation Scribe – @nvidia*
