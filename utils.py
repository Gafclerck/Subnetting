from validate import validate_cidr, validate_ip, validate_ip_bin, CidrError


# Conversion d'un nombre binaire en base 10 2
def base10(binaires):
    """Convertit un nombre binaire (sous forme de chaîne ou d'entier) en nombre décimal.

    Args:
        binaires: Nombre binaire à convertir (peut être une chaîne ou un entier)

    Returns:
        int: Le nombre converti en base 10
    """
    return int(str(binaires), 2)


# Conversion d'un nombre décimal en binaire sur 8 bits (octet)
def base2_octet(a):
    """Convertit un nombre décimal en sa représentation binaire sur 8 bits.

    Args:
        a: Nombre décimal à convertir

    Returns:
        str: Chaîne de 8 caractères représentant l'octet en binaire
    """
    return format(a, "08b")


# Conversion d'une adresse IPv4 décimale pointée en binaire
def ip_base2(ip_dec):
    """Convertit une adresse IPv4 décimale pointée en notation binaire pointée.

    Args:
        ip_dec: Adresse IPv4 sous forme décimale pointée (ex: "192.168.1.1")

    Returns:
        str: Adresse IPv4 en notation binaire pointée
    """
    validate_ip(ip_dec)
    liste_octets_str = ip_dec.split(".")
    liste_octets_bin = [base2_octet(int(octet)) for octet in liste_octets_str]
    ip_bin = ".".join(liste_octets_bin)
    return ip_bin


# Conversion d'une adresse IPv4 binaire pointée en décimale
def ip_base10(ip_bin):
    """Convertit une adresse IPv4 binaire pointée en notation décimale pointée.

    Args:
        ip_bin: Adresse IPv4 sous forme binaire pointée (ex: "11000000.10101000.00000001.00000001")

    Returns:
        str: Adresse IPv4 en notation décimale pointée
    """
    validate_ip_bin(ip_bin)
    liste_octets = ip_bin.split(".")
    liste_octets = [str(base10(octet)) for octet in liste_octets]
    ipv4_dec = ".".join(liste_octets)
    return ipv4_dec


# Calcul du masque de sous-réseau à partir de la notation CIDR
def masque_de_s_r(cidr):
    """Convertit une notation CIDR en adresse de masque de sous-réseau décimale pointée.

    Exemple: /24 → "255.255.255.0"

    Args:
        cidr: Valeur CIDR (entre 0 et 32)

    Returns:
        str: Adresse du masque de sous-réseau
    """
    return add_reseau("255.255.255.255", cidr)


def separateur_add(ad, cidr):
    """Sépare une adresse IP en partie réseau et partie hôte selon le CIDR.

    Args:
        ad: Adresse IPv4 à séparer
        cidr: Valeur CIDR définissant la séparation

    Returns:
        tuple: (partie_réseau, partie_hôte) sous forme de chaînes binaires
    """
    validate_ip(ad)
    validate_cidr(cidr)
    ad_dec = ip_base2(ad)
    l1 = ad_dec.split(".")
    l1 = "".join(l1)
    net_part = l1[:cidr]
    host_part = l1[cidr:]
    return net_part, host_part


def reconstructeur_add(net_part, host_part):
    """Reconstruit une adresse IPv4 à partir de ses parties réseau et hôte en binaire.

    Args:
        net_part: Partie réseau sous forme binaire
        host_part: Partie hôte sous forme binaire

    Returns:
        str: Adresse IPv4 reconstruite en notation décimale pointée
    """
    l1 = net_part + host_part
    l2 = []
    octet = ""
    for i in range(len(l1)):
        octet += l1[i]
        if len(octet) == 8:
            l2.append(octet)
            octet = ""
    l2 = [str(base10(i)) for i in l2]
    add = ".".join(l2)
    return add


def add_reseaux(ad, cidr, replace_bit):
    """Calcule une adresse réseau ou broadcast en remplaçant les bits hôtes.

    Args:
        ad: Adresse IPv4 de départ
        cidr: Valeur CIDR
        replace_bit: 0 pour adresse réseau, 1 pour adresse broadcast

    Returns:
        str: Adresse réseau ou broadcast calculée
    """
    net_part, host_part = separateur_add(ad, cidr)
    if replace_bit == 1:
        host_part = len(host_part) * "1"
    elif replace_bit == 0:
        host_part = len(host_part) * "0"

    add = reconstructeur_add(net_part, host_part)
    return add


def add_reseau(ad, bits):
    """Calcule l'adresse réseau à partir d'une adresse IP et d'un CIDR.

    Args:
        ad: Adresse IPv4
        bits: Valeur CIDR

    Returns:
        str: Adresse réseau calculée
    """
    network = add_reseaux(ad, bits, 0)
    return network


def add_diff(ad, bits):
    """Calcule l'adresse broadcast à partir d'une adresse IP et d'un CIDR.

    Args:
        ad: Adresse IPv4
        bits: Valeur CIDR

    Returns:
        str: Adresse broadcast calculée
    """
    broadcast = add_reseaux(ad, bits, 1)
    return broadcast


def extreme_add(ad, cidr, replace_bit, end_replace):
    """Calcule la première ou dernière adresse utilisable d'un sous-réseau.

    Args:
        ad: Adresse IPv4
        cidr: Valeur CIDR
        replace_bit: Bit de remplacement principal
        end_replace: Bit de remplacement final

    Returns:
        str: Adresse calculée

    Raises:
        ValueError: Si les paramètres de remplacement sont invalides
    """
    net_part, host_part = separateur_add(ad, cidr)
    if replace_bit == 1 and end_replace == 0:
        host_part = (len(host_part) - 1) * "1" + str(end_replace)
    elif replace_bit == 0 and end_replace == 1:
        host_part = (len(host_part) - 1) * "0" + str(end_replace)
    else:
        raise ValueError("Paramètres de remplacement invalides")

    add = reconstructeur_add(net_part, host_part)
    return add


def first_add(ad, cidr):
    """Retourne la première adresse utilisable dans un sous-réseau.

    Args:
        ad: Adresse IPv4
        cidr: Valeur CIDR

    Returns:
        str: Première adresse utilisable
    """
    if cidr == 31:
        return add_reseau(ad, cidr)
    validate_ip(ad)
    validate_cidr(cidr)
    sort = extreme_add(ad, cidr, 0, 1)
    return sort


def last_add(ad, cidr):
    """Retourne la dernière adresse utilisable dans un sous-réseau.

    Args:
        ad: Adresse IPv4
        cidr: Valeur CIDR

    Returns:
        str: Dernière adresse utilisable
    """
    if cidr == 31:
        return add_diff(ad, cidr)
    validate_ip(ad)
    validate_cidr(cidr)
    sort = extreme_add(ad, cidr, 1, 0)
    return sort


class IpAddress:
    """Représente une adresse IP avec toutes ses informations associées.

    Attributes:
        ip: Adresse IPv4
        cidr: Notation CIDR

    Methods fournissant:
        - La notation CIDR
        - La représentation binaire
        - L'adresse réseau
        - L'adresse broadcast
        - La première et dernière adresse utilisable
        - Le masque de sous-réseau
        - Le nombre d'adresses disponibles
    """

    def __init__(self, ip, cidr):
        self.ip = ip
        self.cidr = cidr

    def __str__(self):
        return f"{self.ip}/{self.cidr}"

    def cidr_notation(self):
        """Retourne la notation CIDR sous forme de chaîne."""
        return f"/{self.cidr}"

    def bin_ip(self):
        """Retourne l'adresse IP en notation binaire pointée."""
        return ip_base2(self.ip)

    def network(self):
        """Retourne l'adresse réseau."""
        return add_reseau(self.ip, self.cidr)

    def bin_network(self):
        """Retourne l'adresse réseau en notation binaire pointée."""
        return ip_base2(self.network())

    def broadcast(self):
        """Retourne l'adresse broadcast."""
        return add_diff(self.ip, self.cidr)

    def first_add(self):
        """Retourne la première adresse utilisable dans le sous-réseau."""
        a = first_add(self.ip, self.cidr)
        return a

    def last_add(self):
        """Retourne la dernière adresse utilisable dans le sous-réseau."""
        b = last_add(self.ip, self.cidr)
        return b

    def host_range(self):
        """Retourne la plage d'adresses utilisables sous forme de chaîne."""
        if self.cidr == 32:
            return self.ip
        return self.first_add() + " - " + self.last_add()

    def subnet_mask(self):
        """Retourne le masque de sous-réseau."""
        return masque_de_s_r(self.cidr)

    def bin_mask(self):
        """Retourne le masque de sous-réseau en notation binaire pointée."""
        return ip_base2(self.subnet_mask())

    def num_addresses(self):
        """Calcule le nombre total d'adresses dans le sous-réseau."""
        if self.cidr == 32:
            return 1
        if self.cidr == 31:
            return 2
        return 2 ** (32 - self.cidr)

    def num_usable_hosts(self):
        """Calcule le nombre d'adresses utilisables (hors réseau et broadcast)."""
        if self.cidr == 32:
            return 1
        if self.cidr == 31:
            return 2
        return self.num_addresses() - 2


def subnets(ad, cidr, cidr_final):
    """Générateur produisant tous les sous-réseaux possibles pour une adresse et un CIDR donnés.

    Args:
        ad: Adresse IPv4 de départ
        cidr: CIDR initial
        cidr_final: CIDR final désiré (doit être supérieur au CIDR initial)

    Yields:
        IpAddress: Objets représentant chaque sous-réseau

    Raises:
        CidrError: Si le CIDR final n'est pas valide
    """
    validate_ip(ad)
    validate_cidr(cidr)
    validate_cidr(cidr_final)
    a = cidr_final - cidr
    if a <= 0:
        raise CidrError(f"CIDR pour le subnetting invalide (doit être supérieur au CIDR initial)")
    ad_dec = ip_base2(ad)
    l1 = ad_dec.replace(".", "")
    net_bits = l1[:cidr]
    host_bits = l1[cidr_final:]
    for i in range(2 ** a):
        subnet_bits = format(i, f"0{a}b")
        l1 = net_bits + subnet_bits + host_bits
        l2 = [l1[k:k + 8] for k in range(0, len(l1), 8)]
        add = ".".join([str(base10(j)) for j in l2])
        add = IpAddress(add, cidr_final)
        yield add