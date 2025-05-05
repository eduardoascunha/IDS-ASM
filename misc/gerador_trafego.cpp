#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstdlib>
#include <ctime>

using namespace std;

int main() {
    srand(time(NULL));

    string ips[] = {"10.0.0.20", "10.0.1.20", "10.0.2.20", "10.0.3.20"};
    string messages[4][2] = {
        {"GET / HTTP/1.1\r\nHost: 10.0.0.20\r\n\r\n", "POST / HTTP/1.1\r\nHost: 10.0.0.20\r\nContent-Length: 0\r\n\r\n"},
        {"GET / HTTP/1.1\r\nHost: 10.0.1.20\r\n\r\n", "POST / HTTP/1.1\r\nHost: 10.0.1.20\r\nContent-Length: 0\r\n\r\n"},
        {"GET / HTTP/1.1\r\nHost: 10.0.2.20\r\n\r\n", "POST / HTTP/1.1\r\nHost: 10.0.2.20\r\nContent-Length: 0\r\n\r\n"},
        {"GET / HTTP/1.1\r\nHost: 10.0.3.20\r\n\r\n", "POST / HTTP/1.1\r\nHost: 10.0.3.20\r\nContent-Length: 0\r\n\r\n"}
    };

    int ports[] = {80, 8080, 8000, 443, 23, 21, 22, 25, 110, 143};

    for(int i = 0; i < 5000; i++) {
        int ip_idx = rand() % 4;
        int port_idx = rand() % 10;
        int msg_idx = rand() % 2;

        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            cerr << "Erro ao criar socket" << endl;
            continue;
        }

        struct sockaddr_in server_addr;
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(ports[port_idx]);
        server_addr.sin_addr.s_addr = inet_addr(ips[ip_idx].c_str());

        if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
            //cerr << "Erro ao conectar ao servidor " << ips[ip_idx] << ":" << ports[port_idx] << endl; // vai dar sempre erro que o sv não tem portas abertas
            close(sock);
        } else {
            const char* message = messages[ip_idx][msg_idx].c_str();
            send(sock, message, strlen(message), 0);
            cout << "Pacote enviado com sucesso para " 
                 << ips[ip_idx] << ":" << ports[port_idx] << endl;
            close(sock);
        }

        sleep(1); 
    }

    cout << "Trafego gerado com sucesso!" << endl;
    return 0;
}
