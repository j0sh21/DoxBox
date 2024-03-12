
# DoxBox - une photobox bitcoin ⚡️ lightning

<p align="center">
<img src="https://raw.githubusercontent.com/j0sh21/DoxBox/main/docs/images/Box.jpeg" width="200">
</p>

Le DoxBox imprime les photos capturées lors de paiements par bitcoin lightning à son portefeuille [LNbits](https://github.com/lnbits/lnbits). 
Vous pouvez l'installer lors de n'importe quel mariage, conférence, meetup ou festival. Nous l'avons construit de manière modulaire afin que vous puissiez facilement voyager avec.

## Exigences Matérielles

- **Raspberry Pi 4** exécutant le système d'exploitation basé sur Debian [disponible sur la page officielle des logiciels de Raspberry Pi](https://www.raspberrypi.com/software/operating-systems/).
- **Appareil photo DSLR** : Canon EOS 450D avec au moins 1Go de carte SD. Si vous utilisez un autre modèle, [assurez-vous de vérifier la compatibilité avec gphoto2 sur le site officiel](http://www.gphoto.org/proj/libgphoto2/support.php).
- **Écran** : Waveshare 10,4 pouces QLED Quantum Dot Display Capacitif (1600 x 720).
- **Imprimante** : Xiaomi-Instant-Photo-Printer-1S, compatible avec le système d'impression CUPS, papier photo de 6 pouces.
- **LED** : Bande LED RGB à 4 canaux, accompagnée d'une planche à pain, de câbles de connexion et de 4 Mosfets pour le contrôle.
- **Matériau de Construction** : Trois feuilles de contreplaqué de 80x80cm ; l'accès à une découpeuse laser peut être avantageux.
- **Matériel d'Assemblage** : 20 ensembles d'aimants d'angle (2 pièces par ensemble), 40 vis de 4mm de diamètre et 120 écrous de 4mm de diamètre pour fixer les composants.
- **Couleur en spray** : 1 bombe de peinture d'apprêt, 4 bombes de la couleur réelle.

  
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

## Journal des modifications pour le projet DoxBox
### Version 0.1, publiée le 25 février 2024

### Fonctionnalités
- Mise à jour de `app.py` pour utiliser de nouveaux cadres et de nouveaux GIFs.
- Intégration de nouveaux GIFs de @arbadacarbaYK, supprimant les cadres d'arrière-plan vides et les filigranes. Les GIFs de compte à rebours ont maintenant un timing constant entre les numéros.
- Ajout de `self.isreplay` pour réinitialiser le compteur de boucle des GIF une seule fois.
- Introduction de nouveaux codes d'erreur de `switch.py` dans la documentation en anglais, allemand et portugais.
- Implémentation du nouvel état 3.5 : Transition vers `img_capture.py` après la fin du premier GIF de sourire.
- Implémentation du nouvel état 3.9 : Photo transférée avec succès depuis la caméra, initiation de la préparation à l'impression.
- Avancement de l'état 4 : Déclenché plus tôt pour commencer l'impression avant que la photo ne soit supprimée de la caméra.
- Refonte de la gestion des erreurs spécifiques à la caméra dans `img_capture.py`.
- Introduction du nombre maximal de tentatives de reprise et des temps d'attente variables pour les erreurs liées à la caméra.

### Améliorations
- Ajout de vérifications de la connectivité réseau avant l'interrogation de l'API LNbits.
- Amélioration et nettoyage du style de sortie de la console.
- Caché le curseur de la souris pour une interface utilisateur plus propre.
- Amélioration de la clarté et du détail des messages de journalisation.
- Suppression des fichiers corrompus et nettoyage général.
- Ajustement des effets LED pour un meilleur retour visuel.

### Corrections
- Correction de `def kill_process()` pour garantir la terminaison correcte du processus.
- Résolution du problème où plusieurs GIFs de sourire pouvaient être affichés simultanément.
- Résolution d'un bug où l'état 204 pouvait rester indéfiniment en attente lors de la vérification des échecs de travaux d'impression.

### Infrastructure
- Création d'un dossier de sortie pour les travaux d'impression. **À FAIRE :** Automatiser la création de dossiers en utilisant `os.mkdir` au lieu d'inclure un dossier vide dans le dépôt.
- **À FAIRE :** Ajuster finement la fonctionnalité de `check_print_job_status`.

## Contribuer

Les contributions au projet sont les bienvenues ! Veuillez consulter les directives de contribution pour savoir comment soumettre des pull requests, signaler des problèmes ou suggérer des améliorations.


## Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
Les contributions au projet sont les bienvenues !

## Remerciements
Un merci spécial à [Ben Arc](https://github.com/arcbtc) pour [LNbits](https://github.com/lnbits/lnbits) et à tous les mainteneurs des bibliothèques et outils externes également utilisés dans ce projet.

 ⚡️ [Pourboire pour ce projet](https://legend.lnbits.com/lnurlp/link/4Wc7ZE) si vous aimez le DoxBox ⚡️

