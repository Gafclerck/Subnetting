```markdown
# IP Subnet Calculator

Un outil complet pour analyser et diviser les sous-réseaux IP, avec une interface en ligne de commande intuitive.

## Fonctionnalités

- 🖥️ Analyse complète d'une adresse IP/CIDR :
  - Adresse réseau et broadcast
  - Plage d'adresses utilisables
  - Masque de sous-réseau (décimal et binaire)
  - Nombre d'hôtes disponibles
- 🔢 Subnetting avancé :
  - Division en sous-réseaux de taille variable
  - Tableau récapitulatif clair
- ✅ Validation robuste des entrées
- 🎨 Affichage coloré et structuré

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/Gafclerck/Subnetting.git
cd Subnetting
```

2. (Optionnel) Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
venv\Scripts\activate     # Sur Windows
```

## Utilisation

```bash
python main.py
```

Exemple d'interaction :
```
========== IP SUBNET CALCULATOR ==========

Entrez l'adresse IP (ex: 192.168.1.3/24 ou 192.168.1.3 par défaut /24): 192.168.1.0
Entrez le CIDR pour le subnetting (optionnel, laisser vide pour ignorer): 26

=========== NETWORK INFORMATION ===========
IP Address              192.168.1.0
IP Address (bin)        11000000.10101000.00000001.00000000
Network Address         192.168.1.0
...
```

## Structure du projet

```
ip-subnet-calculator/
├── main.py            # Script principal
├── utils.py           # Fonctions de calcul réseau
├── validate.py        # Validation des entrées
├── inputs.py          # Gestion des saisies utilisateur
└── README.md          # Ce fichier
```

## Exemples d'utilisation

1. Analyse simple :
```bash
python main.py
> Entrez l'adresse IP: 10.0.0.1/24
```

2. Subnetting :
```bash
python main.py
> Entrez l'adresse IP: 192.168.1.0/24
> CIDR pour subnetting: 26
```

## Dépendances

- Python 3.6+
- Aucune dépendance externe

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

[AMADOU ABDOUL-GAFAR]

## Contribuer

Les contributions sont les bienvenues ! Ouvrez une issue ou soumettez une pull request.
```