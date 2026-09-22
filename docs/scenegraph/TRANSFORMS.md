# SceneGraph transforms

Source :
https://dev.epicgames.com/documentation/fortnite/transforms-in-scene-graph-in-unreal-editor-for-fortnite

SceneGraph utilise les transforms de `/Verse.org/SpatialMath`.

Le système Verse SpatialMath utilise le repère droit **LUF** :

- Left
- Up
- Forward

Un `transform_component` contient notamment le transform local de l'entity.

Ne pas confondre les conventions de coordonnées UEFN/Unreal utilisées ailleurs avec les valeurs LUF utilisées par les transforms Verse SceneGraph.

Toujours vérifier les transformations spatiales en éditeur.
