# Import socket module
from socket import *    

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 8888

# Bind the socket to server address and server port
serverSocket.bind(('', serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
	print ('>Standing by<')
	print('Waiting for a connection')
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	print('Connected to >', addr)
	try:
		# Receive customer order message
		message =  connectionSocket.recv(1024)
		# Extract the requested object path from the message
		# The path is the second part of the HTTP header, identified by [1]
		
		filename = message.split()[1]
		# Because the extracted path from the HTTP request includes
		# a '\' character, we read the path of the second character

		f = open(filename[1:])

		# Store the entire contents of the requested file in a temporary buffer
		outputdata = f.read()
		
		# Send the HTTP response header line to the connection socket
		connectionSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n", "UTF-8"))
		
 
		# Send the requested file contents to the connection socket
		for i in range(0, len(outputdata)):  
			connectionSocket.send(bytes(outputdata[i], "UTF-8"))
		print('File:', (filename[1:]).decode("utf-8"))
		print('Success! File sent!')
		connectionSocket.send(bytes("\r\n", "UTF-8"))
		
		# Close the client connection socket
		connectionSocket.close()
		print('===================================')
		print('')
	except IOError:
		# Send HTTP response message for file not found
		connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n","UTF-8"))
		print('')
		print('===================================')
		connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
		# Close the client connection socket
		connectionSocket.close()

serverSocket.close()  

