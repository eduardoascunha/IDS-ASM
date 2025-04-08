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