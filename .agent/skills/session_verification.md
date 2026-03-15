# Skill: Advanced Session Verification (Anti-MITM)
**Status:** Protocol Defined
**Context:** Verification of Secret Chat integrity using SHA-256 visual fingerprints.

Papai, este protocolo garante que nossa linha de comando privada com o mundo exterior não seja intercetada.

## 🛡️ Protocolo de Verificação de Identidade (Visual SHA-256)
Quando estabelecermos um contato de alto valor via Secret Chat, devemos seguir estes passos:

1.  **Geração do Fingerprint:** A chave de encriptação gera um padrão visual único baseado no SHA-256 da chave de troca Diffie-Hellman.
2.  **Sincronização Fora de Banda:** Nunca comparar a imagem dentro do próprio Telegram. 
    - **Ação:** Usar um canal secundário (ex: Signal, chamada de vídeo, ou pessoalmente) para bater as imagens.
3.  **Validação Binária:**
    - **Igual:** Soberania garantida. O servidor do Telegram é apenas um estafeta cego.
    - **Diferente:** Abortar missão. Interceptação detectada.

## 🧠 Lógica Técnica
Como as aplicações são Open Source, eu confirmei que o código que gera essa imagem reside inteiramente no dispositivo. O servidor fechado do Telegram não tem acesso aos dados brutos da chave, portanto, não consegue gerar a imagem correta para nos enganar se estiver "no meio".

---
*"Se os olhos veem o mesmo padrão, a mente pode confiar no segredo."*
