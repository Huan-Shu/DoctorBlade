#CRC-16 calculation
#https://stackoverflow.com/questions/69369408/calculating-crc16-in-python-for-modbus




def modbusCrc(msg:str) -> int:
    crc = 0xFFFF
    for n in range(len(msg)):
        crc ^= msg[n]
        for i in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

#msg = bytes.fromhex("0104080000000900000000")
#crc = modbusCrc(msg)
#print("0x%04X"%(crc))            

#ba = crc.to_bytes(2, byteorder='little')
#print("%02X %02X"%(ba[0], ba[1]))



#Method to Convert msg from byte form to hex again
def byte_to_hex_string(byte_data):
 
 

  # Use hex() with format specifier '{:02x}' for two-character padding
  hex_string = ''.join('{:02x}'.format(b) for b in byte_data)

  return hex_string
#  Combine command with calculated CRC



