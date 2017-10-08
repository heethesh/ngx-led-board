########################
## DO NOT MODIFY CODE ##
########################

import serial
import time

SERIAL_LIVE = False
DUAL_LINE_TEXT = True

LINE1 = 'BMSCE'
LINE2 = 'TECHNOLOGIES'
final_packet = []

if SERIAL_LIVE:
    ngx = serial.Serial('COM7', 115200, timeout=1)
    print '>>> SERIAL ON\n'
else: print '>>> SERIAL OFF\n'

format_frame = ['\x00', '\x82', '\x00', '\x00', '\x46', '\x4F', '\x52', '\x4D', '\x41', '\x54']
packet_header = ['\x01', '\x00',
                 '\x00', '\x00',
                 '\x57', '\x52', '\x49', '\x54', '\x45',
                 '\x5F',
                 '\x44', '\x41', '\x54', '\x41',
                 '\x00']

if DUAL_LINE_TEXT: packet_header += ['\x02', '\x02']
else: packet_header += ['\x01', '\x01']

line1_header = ['\x00', '\x00', '\x00', '\xff']
line2_header = ['\x01', '\x00', '\x00', '\xff']

def split_to_bytes(integer):
    return [chr(i) for i in divmod(integer, 0x100)]

def write_packet():
    global final_packet
    for i in final_packet:
        ngx.write(i)

def update_checksum():
    global final_packet
    
    calc_sum = 0
    and_sum = 1
    
    for i, char in enumerate(final_packet):
        calc_sum += int(ord(char))

    print 'Checksum Value:', calc_sum
    final_packet[3], final_packet[2] = split_to_bytes(calc_sum)

## GENERATE PACKET ##
final_packet += packet_header
final_packet += line1_header
final_packet += [chr(len(LINE1))] + [i for i in LINE1]
if DUAL_LINE_TEXT:
    final_packet += line2_header
    final_packet += [chr(len(LINE2))] + [i for i in LINE2]
update_checksum()

if SERIAL_LIVE:
    write_packet()
    print '\n>>> PACKET SENT\n'
    ngx.close()
    print '>>> SERIAL OFF\n'

print 'Line 1:', LINE1
print 'Line 2:', LINE2
print '\nPacket Length:', len(final_packet)
print '\nPacket (INT):', [ord(i) for i in final_packet]
print '\nPacket (HEX):', [i for i in final_packet]

########################
## DO NOT MODIFY CODE ##
########################
