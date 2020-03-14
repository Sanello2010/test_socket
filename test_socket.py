import socket
from logging import basicConfig, error, warning
from tabulate import tabulate
import templates


basicConfig(format="%(asctime)s | %(levelname)s | %(message)s")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.19.67", 5000))
server_socket.listen()

table = tabulate(
	tabular_data=[("Egor", 45), ("Pavel", 12), ("Valik", 0)],
	headers=["users", "hours"],
	tablefmt="HTML",
	)

views = {
	'/main': b"HTTP/1.1 200 OK\n\n" + templates.main,
	"/shop": b"HTTP/1.1 200 OK\n\n" + templates.shop,
	"/users": ("HTTP/1.1 200 OK\n\n" + table).encode("UTF-8")
	}


def get_response(get_request):
	
	if request:
		url = request[0].split()
		if len(url) > 1:
			url = url[1]
		else:
			error("url is empty")
			return
		if url == "/favicon.ico":
			error("/favicon.ico")
			return
		return views.get(url, b"HTTP/1.1 404 Not found\n\nNof found")


def sender(client, msg):
	if msg:
		client.sendall(msg)
	client.close()


while True:
	client, addr = server_socket.accept()
	warning(f"accept client by addr {addr}")
	msg = client.recv(4096)
	request = msg.decode("UTF-8").split("\n")
	response = get_response(request)
	sender(client, response)
