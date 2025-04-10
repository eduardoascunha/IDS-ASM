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
        "response": [
            "Registar o IP atacante em logs.",
            "Adicionar regra na firewall para bloquear IP temporariamente:",
            "iptables -A INPUT -s {attacker_ip} -j DROP",
            "Enviar alerta ao administrador."
        ]
    },
    "ping_flood": {
        "response": [
            "Limitar taxa de pacotes ICMP com iptables:",
            "iptables -A INPUT -p icmp -m limit --limit 1/s --limit-burst 5 -j ACCEPT",
            "iptables -A INPUT -p icmp -j DROP",
            "Registrar o IP atacante."
        ]
    },
    "syn_flood": {
        "response": [
            "Ativar SYN cookies no sistema:",
            "sysctl -w net.ipv4.tcp_syncookies=1",
            "Adicionar regra na firewall para limitar conexões:",
            "iptables -A INPUT -p tcp --syn -m limit --limit 10/s --limit-burst 20 -j ACCEPT",
            "iptables -A INPUT -p tcp --syn -j DROP"
        ]
    },
    "dns_flood": {
        "response": [
            "Limitar taxa de pacotes UDP para porta 53:",
            "iptables -A INPUT -p udp --dport 53 -m limit --limit 10/s --limit-burst 15 -j ACCEPT",
            "iptables -A INPUT -p udp --dport 53 -j DROP",
            "Registrar origem e notificar administrador."
        ]
    },
    "http_flood": {
        "response": [
            "Bloquear IP atacante com iptables:",
            "iptables -A INPUT -p tcp --dport 80 -s {attacker_ip} -j DROP",
            "Opcional: usar fail2ban para automatizar bloqueios futuros.",
            "Enviar notificação ao administrador."
        ]
    }
}
