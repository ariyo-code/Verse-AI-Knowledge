# Installation UEFN MCP

Source officielle :
https://dev.epicgames.com/documentation/fortnite/uefn-mcp

Dernière vérification : 2026-09-22.

## Capacités officielles

UEFN MCP permet notamment à un agent compatible MCP de :

- lire et écrire des fichiers Verse ;
- compiler Verse ;
- créer/modifier des entités Verse Scene Graph ;
- parcourir, placer et configurer des Creative devices ;
- démarrer, arrêter et inspecter une session.

## Prérequis

1. Activer **Python Editor Scripting**.
2. Activer **UEFN MCP Toolsets**.
3. Configurer l'auto-start MCP.
4. Générer la configuration client.
5. Démarrer l'agent depuis la racine projet/workspace indiquée.

## Endpoint local utilisé par Epic

```text
http://127.0.0.1:8000/mcp
```

Le port peut être changé dans les préférences UEFN.

## Exemple JSON fourni par Epic

```json
{
  "mcpServers": {
    "unreal-mcp": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

Ne pas supposer que tous les clients utilisent ce format.

## Codex CLI

Epic indique que Codex utilise une configuration TOML et que sa génération n'écrase pas une configuration existante.

Donc :
- laisser UEFN générer la config adaptée ;
- supprimer une config périmée avant régénération si nécessaire ;
- ne pas inventer de TOML non vérifié.

## Dépannage

- lancer l'agent depuis la bonne racine ;
- vérifier Python Editor Scripting ;
- vérifier UEFN MCP Toolsets ;
- vérifier le port ;
- redémarrer UEFN si nécessaire.

## Problèmes connus

Epic documente notamment :
- un risque de confusion XYZ / LUF pour certaines transformations ;
- des hitches/freezes possibles pendant certains appels MCP.

Toujours vérifier visuellement les changements spatiaux.
