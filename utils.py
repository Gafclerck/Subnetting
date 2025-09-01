from validate import validate_ip
import  ipaddress as ipad

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
    liste_octets_bin = [format(int(octet), "08b") for octet in liste_octets_str]
    ip_bin = ".".join(liste_octets_bin)
    return ip_bin


class IpAddress(ipad.IPv4Network):
    """Représente un réseau IPv4 avec toutes ses informations associées.

    Hérite de IPv4Network et ajoute des méthodes supplémentaires pour
    l'analyse et l'affichage des informations réseau.

    Attributes:
        cidr (int): Longueur du préfixe CIDR (de 0 à 32)
        first_address (IPv4Address): Première adresse IP utilisable du réseau
        last_address (IPv4Address): Dernière adresse IP utilisable du réseau
    """

    def __init__(self, ip):
        """Initialise l'objet réseau IPv4.

        Args:
            ip (str): Adresse IP avec notation CIDR (ex: "192.168.1.0/24")

        Raises:
            ValueError: Si l'adresse IP est invalide ou mal formatée
        """
        super().__init__(ip, strict=False)
        self.cidr = self.prefixlen
        self.first_address = list(self.hosts())[0]
        self.last_address = list(self.hosts())[-1]

    def bin_network(self):
        """Retourne l'adresse réseau en notation binaire pointée.

        Returns:
            str: Adresse réseau en format binaire (ex: "11000000.10101000.00000001.00000000")
        """
        return ip_base2(str(self.network_address))

    def host_range(self):
        """Retourne la plage d'adresses IP utilisables.

        Returns:
            str: Plage d'adresses utilisables (ex: "192.168.1.1 - 192.168.1.254")
            IPv4Address: L'adresse elle-même pour un /32
        """
        if self.cidr == 32:
            return self.network_address
        return f"{self.first_address} - {self.last_address}"

    def bin_netmask(self):
        """Retourne le masque de sous-réseau en notation binaire pointée.

        Returns:
            str: Masque de sous-réseau en binaire (ex: "11111111.11111111.11111111.00000000")
        """
        return ip_base2(str(self.netmask))

    def num_usable_hosts(self):
        """Calcule le nombre d'adresses IP utilisables.

        Note: Pour les réseaux /31 (RFC 3021), les deux adresses sont utilisables.
              Pour les réseaux /32, une seule adresse est utilisable.

        Returns:
            int: Nombre d'adresses utilisables dans le réseau
        """
        if self.cidr == 32:
            return 1
        elif self.cidr == 31:
            return 2
        else:
            return self.num_addresses - 2