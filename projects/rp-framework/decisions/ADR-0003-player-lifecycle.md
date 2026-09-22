# ADR-0003 — Player lifecycle obligatoire

Status: accepted-for-template

Tout système lié à un joueur doit définir :

- initialisation des joueurs déjà présents ;
- join ;
- leave ;
- respawn si pertinent ;
- cleanup subscriptions ;
- cleanup async tasks ;
- cleanup UI.

Un système qui ignore le départ joueur n'est pas considéré terminé.
