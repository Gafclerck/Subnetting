import re


class IpError(ValueError):
    """Exception levée lorsqu'une adresse IP est invalide."""
    pass


class CidrError(ValueError):
    """Exception levée lorsqu'une notation CIDR est invalide."""
    pass


def validate_cidr(cidr):
    """Valide qu'une notation CIDR est correcte.

    Args:
        cidr: Notation CIDR à valider (doit être un entier entre 1 et 32)

    Raises:
        CidrError: Si le CIDR n'est pas un entier valide ou hors limites
    """
    if not str(cidr).isdigit():
        raise CidrError(f"CIDR invalide (doit être un entier) : {cidr}")
    if int(cidr) > 32 or int(cidr) <= 0:
        raise CidrError(f"CIDR invalide : doit être compris entre 1 et 32 : {cidr}")


def validate_ip(ip):
    """Valide le format d'une adresse IPv4 décimale pointée.

    Args:
        ip: Adresse IPv4 à valider (peut inclure une notation CIDR optionnelle)

    Raises:
        IpError: Si l'adresse IP ne correspond pas au format attendu

    Note:
        L'expression régulière accepte les formats:
        - 192.168.1.1
        - 192.168.1.1/24
    """
    ip_regex = r"^((?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}" \
               r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)" \
               r"(?:/([1-9]|[12]\d|3[0-2]))?$"
    if not re.fullmatch(ip_regex, ip):
        raise IpError(f"Adresse IP invalide : {ip}")


def validate_ip_bin(ip_bin):
    """Valide le format d'une adresse IPv4 binaire pointée.

    Args:
        ip_bin: Adresse IPv4 en notation binaire pointée à valider

    Raises:
        IpError: Si l'adresse binaire ne correspond pas au format attendu

    Note:
        L'expression régulière attend le format:
        - 11000000.10101000.00000001.00000001
    """
    ip_regex = r"^([01]{8}[.]){3}([01]{8})$"
    if not re.fullmatch(ip_regex, ip_bin):
        raise IpError(f"Erreur IP binaire : adresse invalide : {ip_bin}")