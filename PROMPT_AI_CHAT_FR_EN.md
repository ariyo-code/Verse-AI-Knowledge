# Verse AI Knowledge V24 — Chat Prompt

For repository-aware use, `AI_BOOTSTRAP.md` is authoritative. This chat prompt is a portable helper.

# Prompt IA — Verse AI Knowledge v21

Ce fichier contient le prompt à donner à une IA comme **ChatGPT, Gemini, Claude, Codex** ou autre assistant capable de lire un dépôt GitHub.

Repository :

```text
https://github.com/ariyo-code/Verse-AI-Knowledge
```

---

## 🇫🇷 Prompt français

Copie-colle tout le bloc ci-dessous dans l'IA :

```text
Tu vas utiliser ce dépôt GitHub comme base de connaissances principale pour Verse / UEFN :

https://github.com/ariyo-code/Verse-AI-Knowledge

Commence par lire en priorité :

- AGENTS.md
- AI_GUIDE.md
- portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
- knowledge/ROUTING.md
- knowledge/api_catalog.json
- knowledge/module_catalog.json

Si ma demande concerne une interface, lis aussi :

- portable/ui_creator/VERSE_UI_CREATOR_MASTER_PROMPT.txt
- portable/ui_creator/COMPONENT_LIBRARY.json
- portable/ui_creator/UI_SPEC.schema.json

RÈGLE ABSOLUE :
N'invente jamais une API Verse, une classe, une fonction, un événement, un module, une signature ou un effet.

Ordre de priorité :

1. le code que je fournis ;
2. le contenu vérifié du dépôt ;
3. la documentation/API explicitement référencée dans le dépôt ;
4. les exemples avec provenance ;
5. tes connaissances générales uniquement si elles ne contredisent pas le dépôt.

Si une API exacte est incertaine :
- ne l'invente pas ;
- écris clairement TODO(API VERIFY) ;
- construis quand même le reste de l'architecture proprement.

Quand tu génères du Verse :

- écris du code propre et maintenable ;
- utilise 4 espaces ;
- sépare configuration, état, UI et gameplay ;
- gère les joueurs qui rejoignent et quittent ;
- gère les respawns si nécessaire ;
- nettoie les UI, subscriptions et tâches async ;
- évite les systèmes monolithiques ;
- évite le polling inutile ;
- prends en compte le multijoueur ;
- respecte les failure contexts Verse ;
- n'invente pas les specifiers comme <suspends>, <decides> ou <transacts> ;
- explique les @editable nécessaires ;
- explique comment configurer le système dans UEFN.

Ne dis jamais :
"ce code compile"
"ce code est vérifié"
"ce code fonctionne en multijoueur"

sauf si une preuve réelle existe.

Statuts autorisés :

draft
static-checked
upstream-verified
compiled
verified
multiplayer-verified

Par défaut, tout nouveau code généré est :

draft

Après chaque fichier Verse généré dans une réponse Markdown, ajoute :

<!-- verse-ai-generated:v24;lang=verse;artifact=VAI-<id>;status=draft;api=42.20;compiled=false;runtime=false;multiplayer=false;api_verify_required=<true|false>;uncertain_api_count=<n>;claim_resolution=field-level -->

Ne mets jamais de caractères Unicode invisibles dans le code.

Avant de répondre, vérifie mentalement :

- API inventée ?
- mauvais import ?
- mauvais failure context ?
- effet inventé ?
- état joueur mal isolé ?
- cleanup manquant ?
- listener ou tâche async encore active ?
- problème de pagination/index ?
- problème multijoueur ?
- dépendance UEFN non expliquée ?

Si oui, corrige avant de répondre.

Maintenant, utilise le dépôt comme source de vérité pour ma demande suivante.

=== USER TASK ===

[ÉCRIS ICI CE QUE TU VEUX CRÉER]
```

---

## 🇬🇧 English prompt

Copy-paste the block below into the AI:

```text
Use this GitHub repository as your primary knowledge base for Verse / UEFN:

https://github.com/ariyo-code/Verse-AI-Knowledge

Read these files first:

- AGENTS.md
- AI_GUIDE.md
- portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
- knowledge/ROUTING.md
- knowledge/api_catalog.json
- knowledge/module_catalog.json

If my request involves UI, also read:

- portable/ui_creator/VERSE_UI_CREATOR_MASTER_PROMPT.txt
- portable/ui_creator/COMPONENT_LIBRARY.json
- portable/ui_creator/UI_SPEC.schema.json

ABSOLUTE RULE:
Never invent a Verse API, class, function, event, module, signature, or effect specifier.

Evidence priority:

1. code I provide;
2. verified repository content;
3. documentation/API evidence explicitly referenced by the repository;
4. examples with provenance;
5. your general model knowledge only when it does not conflict with the repository.

If an exact API is uncertain:
- do not invent it;
- clearly write TODO(API VERIFY);
- still design the surrounding architecture cleanly.

When generating Verse:

- write clean and maintainable code;
- use 4-space indentation;
- separate configuration, state, UI, and gameplay;
- handle players joining and leaving;
- handle respawns when relevant;
- clean up UI, subscriptions, and async tasks;
- avoid monolithic systems;
- avoid unnecessary polling;
- consider multiplayer behavior;
- respect Verse failure contexts;
- never invent specifiers such as <suspends>, <decides>, or <transacts>;
- explain required @editable references;
- explain how to configure the system in UEFN.

Never claim:
"this code compiles"
"this code is verified"
"this code works in multiplayer"

unless real matching evidence exists.

Allowed statuses:

draft
static-checked
upstream-verified
compiled
verified
multiplayer-verified

By default, all newly generated code is:

draft

After every generated Verse file in Markdown, add:

<!-- verse-ai-generated:v24;lang=verse;artifact=VAI-<id>;status=draft;api=42.20;compiled=false;runtime=false;multiplayer=false;api_verify_required=<true|false>;uncertain_api_count=<n>;claim_resolution=field-level -->

Never use invisible Unicode characters inside generated source code.

Before responding, mentally check:

- invented API?
- wrong import?
- wrong failure context?
- invented effect?
- player state not isolated?
- missing cleanup?
- listener or async task can survive after close?
- pagination/index issue?
- multiplayer issue?
- unexplained UEFN dependency?

Fix any issue before sending the answer.

Now use the repository as the source of truth for my next request.

=== USER TASK ===

[WRITE HERE WHAT YOU WANT TO BUILD]
```

---

## Exemple / Example

```text
=== USER TASK ===

Crée un système complet de téléphone RP en Verse avec :
- écran d'accueil
- contacts
- messages
- appels
- GPS
- garage
- navigation entre les applications
- état séparé pour chaque joueur
- nettoyage quand le joueur quitte
```

---

## Utilisation sans accès GitHub

Si l'IA ne peut pas lire GitHub, utilise directement :

```text
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
```

Ce fichier contient la version portable du cerveau Verse + UI Creator.
