# STAGE L3 Informatique

4 grands objectifs :

- Détecter les os d'un corps depuis une caméra.
- Enregistrer ces mouvements.
- Animer un rig dans blender avec ces mouvements.
- Créer une IA pour corriger les mouvements d'arts martiaux.

## Prerequis

Avoir python d'installé.
Ici fonctionnel sous la version 3.12.3.

### Installation

Pour pouvoir éxécuter le programme, veuillez être certains de l'installation des modules pythons suivants :

```bash
pip install opencv
pip install mediapipe
```

Vous pouvez ensuite copier le repo

```bash
git clone https://github.com/mrktttt/STAGE-L3.git
```

### Exécution du programme

Avant de commencer la détection, il est fortement recommandé de calibrer la caméra. Pour ça, munissez vous d'un damier fournis ci dessous et commencer la prise de photos (15 à 20 photos minimum).
Puis :

```bash
python3 captureCalibrationImages.py
```

Appuiez sur espace pour prendre une photo.

Ensuite vous pouvez calibrer et tester la calibration dans le programme cameraCalibration.py en exécutant la commande :

```bash
python3 cameraCalibration.py
```

Finalement commencez la détection avec le programme principal :

```bash
python3 detection.py
```

## Auteurs

- Mya Soudain
- Killian Treuil
