import socket
import threading

# 1.socket(set type) 2.bind(port, ip) 3.listen(wait for the connection) 4.accept 5.rec 6.send 7.close
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #1. socket.AF_INET(6) IPv4(6) socket.SOCK_STREAM 流式socket，for TCP   socket.SOCK_DGRAM 数据报式socket，for UDP
#server.setblocking(False)
server.bind(('0.0.0.0',8000))
server.listen()


#
# def handle_input(conn, addr):
#     while True:
#


conn, addr = server.accept()

while True:
    try:
        message = conn.recv(1024)
        print(message.decode('utf-8'))
        
    except BlockingIOError:
        pass
    except NameError:
        continue

    finally:
        if message.decode('utf-8') == 'exit':
            conn.sendall('serverclosed'.encode('utf-8'))

        # conn.close()

        else:
            reply = input('server:')
            conn.sendall(reply.encode('utf-8'))


    # skt.close()

