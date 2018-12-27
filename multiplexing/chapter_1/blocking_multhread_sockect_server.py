import socket
import threading
# 服务器端流程：
# 1.socket(set type)
# 2.bind(port, ip)
# 3.listen(wait for the connection)
# 4.accept
# 5.rec
# 6.send
# 7.close
# socket.socket()入参讲解：
# socket.AF_INET(6) IPv4(6) socket.SOCK_STREAM 流式socket，for TCP
# socket.SOCK_DGRAM 数据报式socket，for UDP


def communication(client):
    while True:
        print(client.recv(1024).decode('utf8'))
        msg = input('reply:')
        client.sendall(msg.encode('utf8'))


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.setblocking(False)
    server.bind(('0.0.0.0', 8000))
    server.listen()
    while True:
        cl, addr = server.accept()
        thread1 = threading.Thread(target=communication, args=(cl,))
        thread1.start()


# 由于把server设置为non-blocking, accept过程都会变成非阻塞，所以需要cpu不断询问
# while True:
#     try:
#         conn, addr = server.accept()
#         conn.setblocking(False)
#     except BlockingIOError as e:
#         pass
#
#     try:
#         message = conn.recv(1024)
#         print(message.decode('utf-8'))
#         if message.decode('utf-8') == 'exit':
#             conn.sendall('serverclosed'.encode('utf-8'))
#             conn.close()
#             break
#
#         else:
#             reply = input('server:')
#             conn.sendall(reply.encode('utf-8'))
#
#     except BlockingIOError:
#         pass
#     except NameError:
#         pass
