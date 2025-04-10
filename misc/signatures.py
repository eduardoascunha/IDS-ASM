# assinaturas de ataques
ATTACK_SIGNATURES = {
    "port_scan": {
        "conditions": {
            "multiple_ports": True,
            "time_window": 5,  # segundos
            "min_attempts": 3
        }
    },
    "ping_flood": {
        "conditions": {
            "protocol": 1,  # ICMP
            "count_threshold": 10,
            "time_window": 1  # segundos
        }
    },
    "syn_flood": {
        "conditions": {
            "protocol": 6,  # TCP
            "count_threshold": 20,
            "time_window": 1  # segundos
        }
    },
    "dns_flood": {
        "conditions": {
            "protocol": 17,  # UDP
            "dst_port": 53,  # Porta DNS
            "count_threshold": 15,
            "time_window": 1
        }
    },
    "http_flood": {
        "conditions": {
            "protocol": 6,  # TCP
            "dst_port": 80,  # Porta HTTP
            "count_threshold": 30,
            "time_window": 1
        }
    }
} 

# assinaturas de defesas
DEFENSE_SIGNATURES = {
    "port_scan": {
        "action": "block_ip",
        "description": "Bloqueia IPs que escaneiam múltiplas portas em um curto intervalo de tempo.",
        "command": lambda ip: f"iptables -A INPUT -s {ip} -j DROP\n"
    },
    "ping_flood": {
        "action": "limit_icmp",
        "description": "Limita a taxa de pacotes ICMP para evitar ataques de flood por ping.",
        "command": lambda ip: f"iptables -A INPUT -p icmp -s {ip} -m limit --limit 1/second --limit-burst 4 -j ACCEPT\n"
                              f"iptables -A INPUT -p icmp -s {ip} -j DROP\n"
    },
    "syn_flood": {
        "action": "tcp_syn_protection",
        "description": "Ativa proteção contra SYN flood usando regras que limitam conexões SYN por segundo.",
        "command": lambda ip: f"iptables -A INPUT -p tcp --syn -s {ip} -m limit --limit 5/second --limit-burst 10 -j ACCEPT\n"
                              f"iptables -A INPUT -p tcp --syn -s {ip} -j DROP\n"
    },
    "dns_flood": {
        "action": "udp_dns_rate_limit",
        "description": "Limita a taxa de requisições DNS por IP para evitar flood na porta 53/UDP.",
        "command": lambda ip: f"iptables -A INPUT -p udp --dport 53 -s {ip} -m limit --limit 5/second --limit-burst 10 -j ACCEPT\n"
                              f"iptables -A INPUT -p udp --dport 53 -s {ip} -j DROP\n"
    },
    "http_flood": {
        "action": "http_conn_limit",
        "description": "Restringe o número de conexões simultâneas HTTP de um único IP.",
        "command": lambda ip: f"iptables -A INPUT -p tcp --dport 80 -s {ip} -m connlimit --connlimit-above 20 -j DROP\n"
    }
}
