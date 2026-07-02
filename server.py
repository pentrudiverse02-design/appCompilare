import socket


def server_app():
    port = int(input('port ul server'))
    while port<0 or port>10000:
        print("introduceti va rog un port ok")
        port = int(input('port ul server'))
    host = '127.0.0.1'
    nrMaxConexiuni=5
    server_socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #facem server de tip TCP
        #eu doresc sa folosesc TCP intrucat vreau sa asigur o siguranta a transmiterii datelor
    server_socker.bind((host,port))
    server_socker.listen(nrMaxConexiuni)
    conn, address = server_socker.recv(1024)
    print(f"Conexiune stabilita cu {str(address)}")
    while True:
        raw=conn.recv(1024)
        if not raw:
            break
        try:
            data=raw.decode('utf-8')
        except:
            print("probleme la decodare de la" + str(address))
            continue
        print(f"am receptionat {data}")
        trimit=input('-> ')
        conn.sendall(trimit.encode())
    conn.close()
    server_socker.close()