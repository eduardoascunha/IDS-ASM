# IDS Multi-Agente

Sistema distribuído de deteção de intrusões em redes, baseado em agentes inteligentes. Combina deteção por assinaturas (ataques conhecidos) e anomalias (machine learning) para identificar e mitigar ataques em tempo real.

## Funcionalidades

- **Arquitetura Multi-Agente**: Monitoriza, analisa e reage a ataques de forma cooperativa.
- **Assinaturas**: Deteta port scan, ping flood, SYN flood, DNS flood e HTTP flood, bloqueando automaticamente IPs maliciosos.
- **Anomalias**: Usa modelos ML treinados para identificar comportamentos suspeitos não catalogados.
- **Expansível**: Assinaturas e regras facilmente configuráveis.
- **Privacidade**: Só analisa cabeçalhos; não armazena pacotes.

## Tecnologias

- Python (SPADE), Openfire (XMPP), CORE (emulador de redes), Scapy, ML (Isolation Forest, One-Class SVM, Autoencoder).

## Estrutura

- **Monitor**: Recolhe tráfego.
- **Análise**: Deteta ataques.
- **Coordenador**: Aplica regras de firewall.
- **Engenheiro**: Valida anomalias.

## Resultados

- Bloqueio automático de ataques simulados.
- Redução de falsos positivos com validação manual.

## Relatório
O relatório encontra-se na diretoria `Rel` e contem informação muito mais detalhada relativamente ao sistema desenvolvido.

**Autores:**  
David Teixeira, Eduardo Cunha, Jorge Rodrigues, Tiago Rodrigues  
Maio 2025

