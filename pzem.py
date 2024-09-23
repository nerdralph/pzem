#!/usr/bin/env python
# requires python3, pymodbus, and pyserial
# reads Peacefair power meters
# PZEM-003 and PZEM-017 DC power meters
# PZEM-004, PZEM-014, and PZEM-016 AC power meters
# http://en.peacefair.cn/products.html

import argparse
import sys

from pymodbus.client import ModbusSerialClient
import serial.tools.list_ports as lp

SADDR = 1                               # default slave address
debug = False

# parse CLI args
def cli_args():
    global debug
    p = argparse.ArgumentParser(description="reads Peacefair power meters")
    p.add_argument("-a", "--addr", help="slave address", type=int, default=argparse.SUPPRESS)
    p.add_argument("-p", "--port")
    p.add_argument("-d", "--debug", action="store_true")
    args=vars(p.parse_args())
    debug=args.pop("debug")
    if debug:
        print("CLI args:", args)
    return args

# read input regs starting at address 0
def input_regs(port: str, addr: int, count: int):
    if not port:
        port = lp.comports()[0].device
    if debug:
        print("Using port", port)
    modbus = ModbusSerialClient(port=port, baudrate=9600, stopbits=2)
    modbus.connect()
    if debug:
        print(modbus)
    return modbus.read_input_registers(0, count=count, slave=addr)

# read PZEM-003 family registers
# return map of register values
def regs_003(port: str="", addr: int=SADDR) -> dict:
    rsp = input_regs(port=port, addr=addr, count=8)
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
    rsp = input_regs(port=port, addr=addr, count=10)
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

