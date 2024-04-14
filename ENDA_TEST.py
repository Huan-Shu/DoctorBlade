# Author:           HUAN
# Date:             2024-08-04
# Last modified:    2024-08-04


#ENDA_HEATER = 5500
#ENDA_READER = 5501


import socket
# The IP address of your WaveShare device
HOST = "192.168.27.31"

# The port number used by your WaveShare device (common options: 80, 23)
PORT = 26  # Assuming it uses a web server

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    print("Connected to WaveShare device successfully!")
except ConnectionRefusedError:
    print("Connection failed! Check the IP address and port.")
    exit()

# Replace "your_hex_command" with the actual hex string of your command
hex_command = "010600000046"

#Combine command with calculated CRC16
import CRC16
msg = bytes.fromhex(hex_command)
crc = CRC16.modbusCrc(msg)          
ba = crc.to_bytes(2, byteorder='little')
hex_command = CRC16.byte_to_hex_string(msg) +"%02X%02X" %(ba[0], ba[1])

# Convert hex string to byte array
command_bytes = bytearray.fromhex(hex_command)


# Send the command
sock.sendall(command_bytes)

# ... (Optional: Receive response if applicable)



# Close the connection
sock.close()
print("Connection closed.")




    

    
    
    
