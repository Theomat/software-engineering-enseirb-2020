# Quels objectifs pour notre modèle ?

Reprenons la matrice de confusion pour le recall :
![confusion matrix](https://raw.githubusercontent.com/Theomat/software-engineering-enseirb-2020/main/exercice2/original_confusion_matrix.png)

Et le rapport plus général :
```
TEST:
                   precision    recall  f1-score   support

   find-around-me       0.88      0.43      0.58        67
      find-flight       0.88      0.29      0.44        24
       find-hotel       0.78      0.38      0.51        55
  find-restaurant       0.98      0.56      0.71        93
       find-train       0.93      0.67      0.78        21
       irrelevant       0.79      0.98      0.87       677
provide-showtimes       0.80      0.29      0.42        14
         purchase       0.79      0.59      0.67       114

         accuracy                           0.80      1065
        macro avg       0.85      0.52      0.62      1065
     weighted avg       0.82      0.80      0.78      1065
```

## Objectifs principaux


Nous allons donner les objectifs généraux, néanmoins cela se révélera très vague car sans précision, on ne cherche ici qu'à développer les idées.


On veut que:
1. l'utilisateur ne soit pas piégé dans une démarche qui ne correspond pas à son intention
2. l'utilisateur arrive dans la bonne démarche

L'objectif 1. se traduit de plusieurs façon.
En premier lieu, cela implique que si l'on n'est pas sûr de l'intention de l'utilisateur, on préferera dire que l'intention est 'irrelevant'.
En second lieu, avec l'objectif 2., cela veut dire qu'on veut un fort recall, ce qui représente que toutes les données appartenant à une classe doivent être le moins possible associées à une autre classe (hormis à la classe "irrelevant", ce qui s'observera dans les matrices de confusion).

Enfin, on veut un taux de faux positif très bas pour les classes autres que 'irrelevant', pour s'assurer que l'utilisateur ne se lance pas dans une démarche non souhaitée.
Ce taux de faux positif bas se traduit par une forte précision.


Maintenant, que les objectifs ont été identifiés, il faut placer les plages de valeurs que l'on souhaite atteindre.

## Traduction des objectifs

La précision la plus basse avec le modèle initial est de 0.78, on aimerait donc faire monter se seuil à 0.85, et essayer de viser une moyenne pondérée de 0.90 sur la précision.

Le recall le plus bas est de 0.29 dans le modèle d'origine, là on veut une forte amélioration, on aimerait ici aussi que la plus bas atteigne 0.80 avec une moyenne pondérée à 0.85.

Le cas particulier de 'irrelevant', on veut dans la matrice de confusion normalisée pour le recall, que les éléments non diagonaux soient inférieurs à 0.05 exceptés pour la colonne 'irrelevant'.
On veut un recall élevé pour 'irrelevant' mais pour la précision, on s'autorise une valeur plus faible puisque l'on préfère classer en 'irrelevant' si l'on n'est pas suffisamment sûr de l'intention utilisateur, ce qui se traduit en une augmentation du taux de faux positif.
