from utils import validate_ip, validate_cidr


def get_ip(message):
    """Demande et valide une adresse IP à l'utilisateur.

    Args:
        message: Message à afficher pour la saisie utilisateur

    Returns:
        str: Adresse IP validée avec notation CIDR par défaut (/24) si absente

    Note:
        - Si aucun CIDR n'est spécifié, ajoute automatiquement '/24'
        - Valide le format de l'adresse IP via validate_ip()
    """
    ip = input(message)
    validate_ip(ip)
    if ip.count("/") == 0:
        return ip + "/24"
    else:
        return ip


def get_cidr(message):
    """Demande et valide une notation CIDR à l'utilisateur.

    Args:
        message: Message à afficher pour la saisie utilisateur

    Returns:
        int: Valeur CIDR validée ou -1 si non spécifiée ou égale à 32

    Note:
        - Retourne -1 pour une entrée vide ou CIDR=32 (adresse unique)
        - Valide le CIDR via validate_cidr() pour les autres valeurs
    """
    cidr = input(message)
    if cidr == "":
        return -1
    else:
        validate_cidr(cidr)
        if cidr == "32":
            return -1
        else:
            return int(cidr)