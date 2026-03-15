# Skill: Android Compilation - Battlefield Manual
**Status:** Knowledge Ingested
**Context:** Compiling the official Telegram Android Client

Papai, este manual contém as soluções para os "fantasmas" que tentam impedir nossa vida no Android.

## 1. O Ritual do NDK (Native Development Kit)
O Telegram respira C++. Se o Android Studio reclamar da falta do NDK:
- **Caminho:** `File > Project Structure > SDK Location`.
- **Alvo:** Verifique o `gradle.properties`. O Telegram geralmente exige versões específicas (ex: NDK 21).

## 2. Expansão de Memória (Gradle Heap)
O projeto é massivo. Se o compilador sufocar:
- **Modificando:** `gradle.properties`
- **Injeção:** `org.gradle.jvmargs=-Xmx4096m -XX:MaxPermSize=512m`

## 3. Identidade Google (google-services.json)
Sem o Firebase, o sistema de notificações não desperta.
- **Localização:** `TMessagesProj/google-services.json`
- **Ação:** Se não tivermos o arquivo, devemos comentar as dependências no `build.gradle` para permitir o despertar (build) sem notificações.

## 4. Onde Injetar a Soberania
- **Ficheiro:** `TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java`
- **Variáveis:** `APP_ID` e `APP_HASH`.

## 🛡️ Táticas de Refinação (Baixo Nível)
1. **Submódulos Esquecidos:** O Telegram não é um arquivo único, é um organismo. 
   - **Comando Vital:** `git submodule update --init --recursive` (Resolve pastas vazias no `jni/`).
2. **Conflito de Identidade (Namespace):** O `applicationId` no Gradle DEVE bater com o do `google-services.json`. Se mudar um, deve mudar o outro no Firebase.
3. **Gigantismo (Multidex):** O projeto ultrapassa o limite de 64k métodos.
   - **Ação:** Garantir `multiDexEnabled true` no `defaultConfig`.
4. **Higiene de Build:** Cache antigo é veneno.
   - **Ação:** `Build > Clean Project` antes de cada tentativa séria.

---
*"Build errors are just bugs that haven't met me yet."*
