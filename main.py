#!/usr/bin/env python3
"""
Script principal pour l'analyse de sous-réseaux IP
Affiche les informations réseau et permet le subnetting
"""

import sys
import utils as ut
from inputs import get_cidr, get_ip
from validate import IpError, CidrError

# Constantes pour les couleurs d'affichage
COLOR_LABEL = "\033[0m"
COLOR_VALUE = "\033[36m"
COLOR_ERROR = "\033[31m"
COLOR_TABLE = "\033[36m"


def display_network_info(ip_address):
    """Affiche les informations détaillées du réseau.

    Args:
        ip_address: Objet IpAddress contenant les informations à afficher
    """
    info_labels = [
        ("Network Address", ip_address.network_address),
        ("Network Address (bin)", ip_address.bin_network()),
        ("Broadcast Address", ip_address.broadcast_address),
        ("First usable Address", ip_address.first_address),
        ("Last usable Address", ip_address.last_address),
        ("Usable IP Range", ip_address.host_range()),
        ("Cidr Notation", ip_address),
        ("Netmask", ip_address.netmask),
        ("Netmask (bin)", ip_address.bin_netmask()),
        ("Number of Hosts", ip_address.num_addresses),
        ("Number of Usable Hosts", ip_address.num_usable_hosts())
    ]

    print("\n" + " NETWORK INFORMATION ".center(50, "=") + "\n")
    for label, value in info_labels:
        print(f"{COLOR_LABEL}{label.ljust(25)}{COLOR_VALUE}{value}")


def display_subnet_table(subnets_list):
    """Affiche un tableau formaté des sous-réseaux.

    Args:
        subnets_list: Liste des objets IpAddress représentant les sous-réseaux
    """

    def print_table_row(a, b, c, fill_char=" "):
        """Affiche une ligne formatée du tableau."""
        a = str(a)
        b = str(b)
        c = str(c)
        print(
            f"{COLOR_TABLE}{a.center(20, fill_char)}|{b.center(40, fill_char)}|{c.center(20, fill_char)}{COLOR_LABEL}")

    print("\n" + " SUBNETTING TABLE ".center(82, "="))
    print_table_row("Subnet Address", "Usable Address Range", "Broadcast Address")
    print_table_row("", "", "", "_")

    for subnet in subnets_list:
        print_table_row(subnet.network_address, subnet.host_range(), subnet.broadcast_address)


def main():
    """Fonction principale du programme."""
    try:
        # Récupération des entrées utilisateur
        ip_input = get_ip("Entrez l'adresse IP (ex: 192.168.1.3/24 ou 192.168.1.3 par défaut /24): ")
        cidr_initial = int(ip_input.split("/")[1])

        cidr_final = get_cidr("Entrez le CIDR pour le subnetting (optionnel, laisser vide pour ignorer): ")
        ip_address = ut.IpAddress(ip_input)

        # Affichage des informations réseau
        display_network_info(ip_address)

        # Gestion du subnetting si demandé
        if cidr_final != -1:
            subnets_list = list(ip_address.subnets(cidr_final - cidr_initial))
            display_subnet_table(subnets_list)

    except (IpError, CidrError) as e:
        print(f"\n{COLOR_ERROR}Erreur de configuration réseau: {e}{COLOR_LABEL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{COLOR_ERROR}Erreur inattendue: {e}{COLOR_LABEL}")
        sys.exit(1)

if __name__ == "__main__":
    print("\n" + " IP SUBNET CALCULATOR ".center(50, "=") + "\n")
    main()