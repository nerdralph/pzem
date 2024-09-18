#!/usr/bin/env python
# requires python3, pymodbus, and pyserial
# reads Peacefair power meters
# PZEM-003 and PZEM-017 DC power meters
# PZEM-004, PZEM-014, and PZEM-016 AC power meters
# http://en.peacefair.cn/products.html

import sys

from pymodbus.client import ModbusSerialClient
import serial.tools.list_ports as lp

SADDR = 1                               # default slave address

def modbus_connect(port: str=""):
    if not port:
        port = lp.comports()[0].device
    modbus = ModbusSerialClient(port=port, baudrate=9600)
    modbus.connect()
    return modbus

# read PZEM-003 family registers
# return map of register values
def regs_003(port: str="", addr: int=SADDR) -> dict:
    modbus = modbus_connect(port)
    # read all regs starting at address 0
    rsp = modbus.read_input_registers(0, count=8, slave=addr)

    regs={
        "volt": rsp.registers[0]/100,
        "amp": rsp.registers[1]/100,
        "watt": rsp.registers[2]/10 + rsp.registers[3]*6553.6,
        "watt-hour": rsp.registers[4] + rsp.registers[5]*65536,
        "HValarm": rsp.registers[6],
        "LValarm": rsp.registers[7]
        }
    return regs

# read PZEM-004 family registers
# return map of register values
def regs_004(port: str="", addr: int=SADDR) -> dict:
    modbus = modbus_connect(port)
    # read all regs starting at address 0
    rsp = modbus.read_input_registers(0, count=10, slave=addr)

    regs={
        "volt": rsp.registers[0]/10,
        "amp": rsp.registers[1]/1000,
        "watt": rsp.registers[3]/10 + rsp.registers[4]*6553.6,
        "watt-hour": rsp.registers[5] + rsp.registers[6]*65536,
        "hertz": rsp.registers[7]/10,
        "pwrfactor": rsp.registers[8]/100,
        "alarm": rsp.registers[9]
        }
    return regs

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(regs_004())
    else:
        print(regs_004(port = sys.argv[1]))

