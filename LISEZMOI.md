
# Doxbox - une photobox bitcoin ⚡️ lightning

<p align="center">
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/7eda15cf-c3a2-4236-9e24-a084b4512d96" width="200">
</p>

Le Doxbox imprime les photos capturées lors de paiements par bitcoin lightning à son portefeuille [LNbits](https://github.com/lnbits/lnbits). 
Vous pouvez l'installer lors de n'importe quel mariage, conférence, meetup ou festival. Nous l'avons construit de manière modulaire afin que vous puissiez facilement voyager avec.

## Matériel Nécessaire

- **Raspberry Pi 4** fonctionnant avec le [firmware debian](https://www.raspberrypi.com/software/operating-systems/)
- **Appareil photo DSLR** : Canon EOS 450D avec au moins 1 Go de carte SD. Si vous utilisez un autre modèle, assurez-vous de la compatibilité avec gphoto2
- **Écran** : Écran capacitif QLED Quantum Dot de Waveshare 10,4 pouces (1600 x 720)
- **Imprimante** : Imprimante photo instantanée Xiaomi-1S, compatible avec CUPS, papier photo 6 pouces
- **LED** : Ligne RGB à 4 pôles, planche à pain, câbles, 4 Mosfets
- **Bois** : 3 panneaux de contreplaqué de 80x80cm, éventuellement une découpeuse laser
- **Aimants** : 20 aimants d'angle (2 pièces chacun), 40 vis de 4mm, 120 écrous de 4mm
- **Peinture en aérosol** : 1 bombe de peinture d'apprêt, 4 bombes de peinture de couleur finale
  
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/384280e0-cc6e-4bd0-9953-c318b5e12f15" height="200">
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/e446af16-d840-4cbc-87f9-3d5f67b3a15d" height="200">
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/4bcc6965-a1fa-41e5-8d07-cc7e3280bc58" height="200">


## Exemple de flux de programme :

<img src="docs/images/flowchart.JPG" height="1100">


## Instructions d'Installation

### Composants Clés

- **main.py** : Sert de point d'entrée de l'application, orchestrant l'exécution des divers composants en fonction des modes opérationnels.
- **app.py** : Gère l'interface utilisateur graphique (GUI) de l'application, facilitant les interactions des utilisateurs et l'affichage des informations.
- **switch.py** : Gère les interactions avec les API externes et effectue des actions spécifiques en fonction des données reçues, telles que le déclenchement d'autres composants de l'application.
- **img_capture.py** : Interagit avec les appareils photo pour capturer des images, les télécharger et gérer le stockage des fichiers, en utilisant gphoto2.
- **print.py (En Cours)** : Interface avec les imprimantes en utilisant CUPS pour imprimer des images, avec la possibilité de sélectionner des imprimantes et de gérer les travaux d'impression.
- **config.py** : Contient les paramètres de configuration utilisés dans toute l'application, tels que les clés API, les noms d'appareils et les chemins de fichiers.

### Installation

1. **Cloner le Répertoire** : Commencez par cloner ce dépôt.

   ```sh
   git clone https://github.com/j0sh21/DoxBox.git
   ```
2. **Installer les Dépendances** : Assurez-vous que Python est installé sur votre système, installez les packages Python requis.

    ```sh
    pip install -r requirements.txt
    ```
    **Note** : Certains composants peuvent nécessiter des dépendances supplémentaires au niveau du système (par exemple, gphoto2, CUPS).
   

   - Si vous souhaitez installer automatiquement des dépendances supplémentaires au niveau du système, exécutez plutôt install.sh :
      ```sh
      cd DoxBox/install
      chmod u+x install.sh
      ./install.sh
     ```

3. **Configurer** : Révisez et mettez à jour config/cfg.ini avec vos paramètres spécifiques, tels que les noms d'appareils, les clés API et les chemins de fichiers.
   ```sh
   nano cfg.ini
## Utilisation

Pour exécuter l'application, naviguez vers le répertoire du projet et exécutez main.py :

 ```sh
python3 main.py
 ```
Pour des fonctionnalités spécifiques, telles que la capture d'une image ou l'impression, vous pouvez exécuter les scripts respectifs (par exemple, python img_capture.py pour la capture d'image).
Exemple d'Utilisation

**Capturer une Image** Assurez-vous que votre appareil photo est connecté et reconnu par votre système, puis exécutez :

 ```sh
python3 img_capture.py
 ```
**Imprimer une Image** : Mettez à jour print.py avec le nom de votre imprimante et le chemin du fichier image, puis exécutez :
 ```sh
 python print.py
 ```

## Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
Les contributions au projet sont les bienvenues !

## Remerciements
Un merci spécial à [Ben Arc](https://github.com/arcbtc) pour [LNbits](https://github.com/lnbits/lnbits) et à tous les mainteneurs des bibliothèques et outils externes également utilisés dans ce projet.

 ⚡️ [Pourboire pour ce projet](https://legend.lnbits.com/lnurlp/link/4Wc7ZE) si vous aimez le DoxBox ⚡️

