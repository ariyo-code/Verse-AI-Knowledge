# Verse-AI-Knowledge
AI knowledge base for Verse / UEFN — grounded prompts, API references, UI tools, RAG and validation. Never invent a Verse API.

<div align="center">

# 🤖 Verse AI Knowledge

### 🇫🇷 Base de connaissances IA pour Verse / UEFN  
### 🇬🇧 AI Knowledge Base for Verse / UEFN

**ChatGPT · Codex · Claude · Gemini · Other capable LLMs**

> 🧠 **Règle principale / Core rule:**  
> **Ne jamais inventer une API Verse. / Never invent a Verse API.**

📦 **Version : v21**  
🎮 **UEFN / Verse focused**  
🧩 **UI Creator included**  
🔐 **Proprietary project license**

</div>

---

# 🇫🇷 Français

## ✨ Qu'est-ce que Verse AI Knowledge ?

**Verse AI Knowledge** est une base de connaissances structurée conçue pour aider les IA comme **ChatGPT, Codex, Claude, Gemini** et d'autres modèles capables de lire un dépôt GitHub à générer du code **Verse / UEFN** plus propre, plus fiable et plus maintenable.

Le projet ne “réentraîne” pas directement une IA.

Il lui fournit plutôt :

- 📚 une base de connaissances Verse / UEFN ;
- 🧠 un Master Prompt spécialisé ;
- 🔎 des règles de recherche et de priorité des sources ;
- 🧩 un créateur d'interfaces UI ;
- 🛡️ des règles anti-hallucination ;
- 🧪 des outils de validation statique ;
- 🗂️ des catalogues d'API et de modules ;
- 🔗 de la provenance pour les sources externes ;
- 🧰 des patterns et exemples de projets ;
- 📊 du RAG, de l'Evidence et des outils VerseLab.

---

## 🚨 Règle absolue

> ### ❌ Ne jamais inventer une API Verse.

Une IA utilisant ce dépôt ne doit jamais inventer :

- une classe ;
- une fonction ;
- un événement ;
- un module ;
- une signature ;
- un effet ;
- un import ;
- une propriété Verse.

Si une API exacte n'est pas vérifiable :

```text
TODO(API VERIFY)
```

doit être utilisé à la place d'une API inventée.

---

## 🚀 Démarrage rapide

### 1️⃣ Donne le dépôt à ton IA

```text
https://github.com/abdullah1552-blip/Verse-AI-Knowledge
```

Puis demande-lui de lire en priorité :

```text
AGENTS.md
AI_GUIDE.md
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
knowledge/ROUTING.md
knowledge/api_catalog.json
knowledge/module_catalog.json
```

### 2️⃣ Pour une interface UI

L'IA doit aussi lire :

```text
portable/ui_creator/VERSE_UI_CREATOR_MASTER_PROMPT.txt
portable/ui_creator/COMPONENT_LIBRARY.json
portable/ui_creator/UI_SPEC.schema.json
```

### 3️⃣ Prompt prêt à copier

Le prompt complet à donner à une IA est disponible ici :

```text
PROMPT_AI_CHAT_FR_EN.md
```

---

## 💬 Exemple de demande

```text
=== USER TASK ===

Crée un système complet de garage RP en Verse.

Fonctionnalités :
- véhicules possédés par joueur ;
- persistance ;
- verrouillage / déverrouillage ;
- clés temporaires ;
- menu de garage ;
- un seul véhicule actif par joueur ;
- gestion des respawns ;
- nettoyage à la déconnexion ;
- compatibilité multijoueur.
```

---

## 🧠 Priorité des connaissances

Quand l'IA doit générer du Verse, elle doit suivre cet ordre :

1. 🥇 le code fourni directement par l'utilisateur ;
2. 🥈 le contenu vérifié du dépôt ;
3. 🥉 les API / documentations référencées dans le dépôt ;
4. 📚 les exemples disposant d'une provenance claire ;
5. 🤖 les connaissances générales du modèle uniquement si elles ne contredisent pas le dépôt.

---

## ✅ Statuts de validation

| Statut | Signification |
|---|---|
| 📝 `draft` | Code généré ou écrit, non validé dans UEFN |
| 🔍 `static-checked` | Vérifications statiques du dépôt effectuées |
| 📚 `upstream-verified` | Soutenu par une source upstream fiable |
| 🛠️ `compiled` | Une vraie compilation UEFN existe |
| ✅ `verified` | Compilé et testé fonctionnellement |
| 🌐 `multiplayer-verified` | Testé dans un contexte multijoueur pertinent |

> ⚠️ Une validation statique ne remplace jamais une vraie compilation UEFN.

Tout nouveau code généré commence par défaut avec :

```text
draft
```

---

## 🧩 UI Creator

Le projet contient un système spécialisé pour créer et structurer des interfaces Verse / UEFN.

### Pipeline

```text
Demande / Image / Référence
            ↓
        UI Spec
            ↓
   Hiérarchie composants
            ↓
       État + événements
            ↓
 Implémentation Verse vérifiée
```

Il inclut :

- 🧱 bibliothèque logique de composants ;
- 🧾 schéma UI structuré ;
- 🎨 création d'interface ;
- ♻️ refonte d'interface ;
- 🖼️ génération depuis une référence visuelle ;
- 🔗 planification des événements ;
- 📱 responsive design ;
- 🧹 refactorisation ;
- 🛡️ règles anti-hallucination des widgets Verse.

Dossier :

```text
portable/ui_creator/
```

---

## 🧠 Master Prompt Verse

Le fichier principal est :

```text
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
```

Il couvre notamment :

- 📦 imports et modules ;
- ⚠️ failure contexts ;
- ⚙️ effets et signatures ;
- 👤 état joueur ;
- 🔄 lifecycle ;
- ⏳ concurrence et tâches async ;
- 🧹 cleanup ;
- 💾 persistance ;
- 🚗 véhicules ;
- 👥 équipes ;
- 🎮 Creative Devices ;
- 🌐 multijoueur ;
- 🧩 UI ;
- 🏗️ architecture maintenable ;
- 🧪 vérification avant réponse.

---

## 🔎 Base de connaissances

Les fichiers principaux sont :

```text
knowledge/ROUTING.md
knowledge/api_catalog.json
knowledge/module_catalog.json
knowledge/index.json
```

Ils permettent à l'IA de savoir :

- où chercher ;
- quelles API sont connues ;
- quels modules sont disponibles ;
- quelles informations nécessitent une vérification supplémentaire.

---

## 🧪 RAG, Evidence & VerseLab

Le projet contient également plusieurs systèmes de recherche, d'analyse et de validation :

```text
rag/
curation/
verification/
reports/
lab/
benchmark/
benchmarks/
tests/
tools/
```

🎯 Objectif : récupérer les meilleures preuves disponibles avant de produire du code.

---

## 🏷️ Marqueur de code généré

Les réponses Markdown peuvent contenir :

```html
<!-- verse-ai-generated:v21;lang=verse;status=draft -->
```

Ce marqueur :

- 👁️ est visible dans le Markdown brut ;
- 🙈 est masqué dans le rendu normal ;
- ✅ utilise uniquement un commentaire HTML standard ;
- ❌ n'ajoute aucun caractère Unicode invisible dans le code Verse.

Le projet interdit volontairement :

- les caractères zero-width ;
- les contrôles bidirectionnels invisibles ;
- les tags Unicode cachés ;
- les identifiants modifiés avec des caractères invisibles.

---

## 📂 Structure du projet

```text
Verse-AI-Knowledge/
├── 📁 .github/
├── 📁 benchmark/
├── 📁 benchmarks/
├── 📁 bridge/
├── 📁 curation/
├── 📁 dependencies/
├── 📁 docs/
├── 📁 errors/
├── 📁 examples/
├── 📁 external/
├── 📁 knowledge/
├── 📁 lab/
├── 📁 maintenance/
├── 📁 mcp/
├── 📁 portable/
│   └── 📁 ui_creator/
├── 📁 projects/
├── 📁 prompts/
├── 📁 rag/
├── 📁 reports/
├── 📁 schemas/
├── 📁 staging/
├── 📁 systems/
├── 📁 templates/
├── 📁 tests/
├── 📁 tools/
├── 📁 verification/
├── 📄 AGENTS.md
├── 📄 AI_GUIDE.md
├── 📄 README.md
├── 📄 README_FR.md
├── 📄 README_EN.md
├── 📄 SECURITY.md
├── 📄 LICENSE.md
├── 📄 THIRD_PARTY_NOTICES.md
├── 📄 VERSION.md
└── 📄 manifest.json
```

---

## 🔐 Sécurité

Ne publie jamais :

- 🔑 clés API ;
- 🎮 identifiants Epic Games ;
- 🤖 token Discord ;
- 🗄️ URL de base de données contenant des identifiants ;
- 🔒 mots de passe ;
- 📄 fichiers `.env` privés ;
- 🪪 tokens d'authentification ;
- 🔐 clés SSH privées.

Voir :

```text
SECURITY.md
```

---

## 📜 Licence

**Verse AI Knowledge n'est pas un projet open-source sauf si le propriétaire du dépôt change explicitement sa licence.**

Les conditions applicables au contenu original du projet sont définies dans :

```text
LICENSE.md
```

Le fait que le dépôt soit public ne donne pas automatiquement le droit de :

- redistribuer le projet ;
- republier le ZIP ;
- créer un mirror public ;
- revendre le projet ;
- republier une copie substantielle ;
- supprimer les mentions de copyright ou de provenance.

Les contenus tiers conservent leurs propres licences.

Voir :

```text
THIRD_PARTY_NOTICES.md
```

---

## ⚠️ Disclaimer

Verse, Unreal Editor for Fortnite, Fortnite, Epic Games ainsi que les marques et technologies associées appartiennent à leurs propriétaires respectifs.

**Verse AI Knowledge est un projet indépendant et n'est ni affilié, ni approuvé, ni sponsorisé par Epic Games.**

Le code généré par une IA peut contenir des erreurs.  
Pour un projet important, compile et teste toujours le code dans UEFN.

---

# 🇬🇧 English

## ✨ What is Verse AI Knowledge?

**Verse AI Knowledge** is a structured knowledge repository designed to help AI assistants such as **ChatGPT, Codex, Claude, Gemini** and other capable models generate cleaner, safer and more maintainable **Verse / UEFN** code.

The repository does not directly retrain an AI model.

Instead, it provides:

- 📚 a Verse / UEFN knowledge base;
- 🧠 a specialized Master Prompt;
- 🔎 source-priority and retrieval rules;
- 🧩 a dedicated UI Creator;
- 🛡️ anti-hallucination rules;
- 🧪 static validation tooling;
- 🗂️ API and module catalogs;
- 🔗 provenance for external sources;
- 🧰 project patterns and examples;
- 📊 RAG, Evidence and VerseLab tooling.

---

## 🚨 Absolute Rule

> ### ❌ Never invent a Verse API.

An AI using this repository must never fabricate:

- a class;
- a function;
- an event;
- a module;
- a signature;
- an effect;
- an import;
- a Verse property.

If an exact API cannot be verified:

```text
TODO(API VERIFY)
```

must be used instead of a fabricated API.

---

## 🚀 Quick Start

### 1️⃣ Give the repository to your AI

```text
https://github.com/abdullah1552-blip/Verse-AI-Knowledge
```

Ask it to read these files first:

```text
AGENTS.md
AI_GUIDE.md
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
knowledge/ROUTING.md
knowledge/api_catalog.json
knowledge/module_catalog.json
```

### 2️⃣ For UI requests

Also read:

```text
portable/ui_creator/VERSE_UI_CREATOR_MASTER_PROMPT.txt
portable/ui_creator/COMPONENT_LIBRARY.json
portable/ui_creator/UI_SPEC.schema.json
```

### 3️⃣ Ready-to-copy AI prompt

Use:

```text
PROMPT_AI_CHAT_FR_EN.md
```

---

## 💬 Example Request

```text
=== USER TASK ===

Create a complete RP garage system in Verse.

Requirements:
- player-owned vehicles;
- persistence;
- lock / unlock;
- temporary keys;
- garage UI;
- one active vehicle per player;
- respawn handling;
- disconnect cleanup;
- multiplayer-safe state.
```

---

## 🧠 Knowledge Priority

When generating Verse, the AI should follow this order:

1. 🥇 code explicitly supplied by the user;
2. 🥈 verified repository content;
3. 🥉 APIs / documentation referenced by the repository;
4. 📚 examples with clear provenance;
5. 🤖 general model knowledge only when it does not conflict with the repository.

---

## ✅ Verification Statuses

| Status | Meaning |
|---|---|
| 📝 `draft` | Written/generated but not validated in UEFN |
| 🔍 `static-checked` | Repository/static checks passed |
| 📚 `upstream-verified` | Supported by trusted upstream evidence |
| 🛠️ `compiled` | Real UEFN compilation evidence exists |
| ✅ `verified` | Compiled and functionally tested |
| 🌐 `multiplayer-verified` | Tested for relevant multiplayer behavior |

> ⚠️ Static validation is never a substitute for a real UEFN compile.

Newly generated code defaults to:

```text
draft
```

---

## 🧩 UI Creator

The repository includes a specialized system for generating and structuring Verse / UEFN interfaces.

### Pipeline

```text
Request / Image / Reference
            ↓
        UI Spec
            ↓
    Component hierarchy
            ↓
       State + events
            ↓
 Verified Verse implementation
```

It includes:

- 🧱 logical component library;
- 🧾 structured UI schema;
- 🎨 UI creation;
- ♻️ UI redesign;
- 🖼️ reference-driven design;
- 🔗 event planning;
- 📱 responsive guidance;
- 🧹 refactoring;
- 🛡️ anti-hallucination rules for Verse UI APIs.

Directory:

```text
portable/ui_creator/
```

---

## 🧠 Verse Master Prompt

Main file:

```text
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
```

It covers:

- 📦 imports and modules;
- ⚠️ failure contexts;
- ⚙️ effects and signatures;
- 👤 player state;
- 🔄 lifecycle;
- ⏳ concurrency and async tasks;
- 🧹 cleanup;
- 💾 persistence;
- 🚗 vehicles;
- 👥 teams;
- 🎮 Creative Devices;
- 🌐 multiplayer;
- 🧩 UI;
- 🏗️ maintainable architecture;
- 🧪 pre-response verification.

---

## 🔎 Knowledge Base

Main files:

```text
knowledge/ROUTING.md
knowledge/api_catalog.json
knowledge/module_catalog.json
knowledge/index.json
```

They help the AI determine:

- where to search;
- which APIs are known;
- which modules are available;
- which claims require additional verification.

---

## 🧪 RAG, Evidence & VerseLab

The repository also contains research, retrieval and validation infrastructure:

```text
rag/
curation/
verification/
reports/
lab/
benchmark/
benchmarks/
tests/
tools/
```

🎯 Goal: retrieve the strongest available evidence before generating Verse code.

---

## 🏷️ Generated-Code Marker

Generated Verse shown in Markdown may include:

```html
<!-- verse-ai-generated:v21;lang=verse;status=draft -->
```

The marker:

- 👁️ is visible in raw Markdown;
- 🙈 is hidden in rendered Markdown;
- ✅ uses a normal HTML comment;
- ❌ does not inject invisible Unicode into Verse source code.

Verse AI Knowledge intentionally avoids:

- zero-width characters;
- bidirectional control characters;
- invisible Unicode tags;
- altered identifiers using invisible characters.

---

## 📂 Repository Structure

```text
Verse-AI-Knowledge/
├── 📁 .github/
├── 📁 benchmark/
├── 📁 benchmarks/
├── 📁 bridge/
├── 📁 curation/
├── 📁 dependencies/
├── 📁 docs/
├── 📁 errors/
├── 📁 examples/
├── 📁 external/
├── 📁 knowledge/
├── 📁 lab/
├── 📁 maintenance/
├── 📁 mcp/
├── 📁 portable/
│   └── 📁 ui_creator/
├── 📁 projects/
├── 📁 prompts/
├── 📁 rag/
├── 📁 reports/
├── 📁 schemas/
├── 📁 staging/
├── 📁 systems/
├── 📁 templates/
├── 📁 tests/
├── 📁 tools/
├── 📁 verification/
├── 📄 AGENTS.md
├── 📄 AI_GUIDE.md
├── 📄 README.md
├── 📄 README_FR.md
├── 📄 README_EN.md
├── 📄 SECURITY.md
├── 📄 LICENSE.md
├── 📄 THIRD_PARTY_NOTICES.md
├── 📄 VERSION.md
└── 📄 manifest.json
```

---

## 🔐 Security

Never publish:

- 🔑 API keys;
- 🎮 Epic Games credentials;
- 🤖 Discord tokens;
- 🗄️ database URLs containing credentials;
- 🔒 passwords;
- 📄 private `.env` files;
- 🪪 authentication tokens;
- 🔐 private SSH keys.

See:

```text
SECURITY.md
```

---

## 📜 License

**Verse AI Knowledge is not an open-source project unless the repository owner explicitly changes the project license.**

Terms for the repository's original content are defined in:

```text
LICENSE.md
```

A public GitHub repository does not automatically grant permission to:

- redistribute the project;
- re-upload ZIP archives;
- create public mirrors;
- resell the project;
- publish substantial copies;
- remove copyright or provenance notices.

Third-party content retains its original licenses.

See:

```text
THIRD_PARTY_NOTICES.md
```

---

## ⚠️ Disclaimer

Verse, Unreal Editor for Fortnite, Fortnite, Epic Games and related trademarks and technologies belong to their respective owners.

**Verse AI Knowledge is an independent project and is not affiliated with, endorsed by or sponsored by Epic Games.**

AI-generated code can contain mistakes.  
Important code should always be compiled and tested in the appropriate UEFN environment.

---

<div align="center">

# 🧠 Verse AI Knowledge v21

### 🇫🇷 Du Verse basé sur des sources, pas sur des API inventées.  
### 🇬🇧 Source-grounded Verse generation. No invented APIs.

⭐ If this project helps you, consider starring the repository.

</div>
