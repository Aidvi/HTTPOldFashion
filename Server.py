import socket
import threading
import os.path


class WebServer:
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("Socket failed with error:: " + err)

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.serverSocket.bind((self.host, self.port))  ## bind Takes turple as first parameter

    def wait_for_connection(self):
        while True:
            self.serverSocket.listen(10)
            client, client_address = self.serverSocket.accept()
            ## Using threads makes it possible for more than one connections at the same time.
            # threading.Thread(target=self.is_connected, args=(client, client_address)).start()
            self.is_connected(client, client_address)

    def get_content(self, my_file):
        response = False
        if os.path.exists(my_file):
            try:
                file = open(my_file, 'rb')
                response = file.read()
                file.close()
            except Exception as e:
                print(e)
        return response

    def write_request_log(self, request, client_address):

        file = open("request_log.txt", "a")
        file.write(request + "FROM ADDRESS :: " + str(client_address) + "\n" + "/" * 90 + "\n")
        file.close()

        file = open("request_log.txt", "r")
        lines = file.readlines()
        file.close()

        lines_keep = []
        for line in lines:
            if not line.isspace():
                lines_keep.append(line)

        file = open("request_log.txt", "w")
        file.write("".join(lines_keep))
        # should also work instead of joining the list:
        # file.writelines(keep)
        file.close()

    def is_connected(self, client, client_address):
        while True:
            request = client.recv(1024).decode('utf-8')
            self.write_request_log(request, client_address)

            list_of_string_request = request.split(" ")
            file_selector = list_of_string_request[1]
            if file_selector == "/":
                file_selector = "/index.html"

            my_file = "." + file_selector

            response = self.get_content(my_file)

            header = 'HTTP/1.1 200 OK\n'

            if not response:
                response = self.get_content("./404.html")
                header = "HTTP/1.1 404 Not Found\n"

            header += 'File:' + my_file + "\n"
            header += 'Connection: close\n\n'

            final_response = header.encode('utf-8')
            final_response += response
            client.sendto(final_response, client_address)
            client.close()
            break


def main():
    server_socket = WebServer("localhost", port=8080)

    server_socket.wait_for_connection()


if __name__ == '__main__':
    main()
