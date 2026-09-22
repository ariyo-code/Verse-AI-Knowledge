# VerseLab One-Click

## Utilisation

Double-clique simplement sur:

`lab/START_VERSELAB.bat`

Le lanceur:

1. vérifie Python;
2. cherche les dossiers `Verse` dans les emplacements UEFN courants;
3. te laisse choisir le bon projet;
4. vérifie VerseLab;
5. place le prochain candidat dans `VAI_LAB/`;
6. génère `lab/generated/AFTER_COMPILE.txt`.

Ensuite, dans UEFN, tu fais uniquement **Build Verse Code**.

Le résultat doit être enregistré avec la commande fournie dans `AFTER_COMPILE.txt`.

## Limite volontaire

Le script ne simule jamais le compilateur Verse.

Il attend un vrai résultat UEFN avant de promouvoir un candidat.
