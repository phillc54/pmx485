#!/usr/bin/python3.11
#FIXME.standalone - above temporarily added for standalone testing

'''
pmx_test.py

Copyright (C) 2020, 2021, 2022, 2023 Phillip A Carter
Copyright (C) 2020, 2021, 2022, 2023 Gregory D Carl

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


Modbus Info: https://www.simplymodbus.ca/ASCII.htm
'''

import os
import sys
import time
from textwrap import wrap as WRAP
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

try:
    import serial
    import serial.tools.list_ports
    sMod = True
except:
    sMod = False

# functions
address         = 0x01
coilRead        = 0x01
regRead         = 0x04
coilWrite       = 0x05
regWrite        = 0x06
regWriteMult    = 0x10

# read registers
rTorchPPS       = (   0x0, 0x3000)
rModeMaxMin     = (   0x0, 0x3001)
rCurrentMin     = (0x2099, 0x3002)
rCurrentMax     = (0x209A, 0x3003)
rPressureMin    = (0x209C, 0x3004)
rPressureMax    = (0x209D, 0x3005)
rModeRead       = (   0x0, 0x3010) # the mode setting
rCurrentRead    = (   0x0, 0x3011) # the current setting
rPressureRead   = (   0x0, 0x3012) # the pressure setting
rCurrentGet     = (   0x0, 0x3018) # the actual current
rPressureGet    = (0x204C, 0x3019) # the actual pressure
rFault          = (0x2098, 0x301A)
rStartsLow      = (   0x0, 0x3028)
rStartsHigh     = (   0x0, 0x3029)
rArcTimeLow     = (0x209E, 0x302A)
rArcTimeHigh    = (0x209F, 0x302B)
rOKLow          = (   0x0, 0x302C)
rOKHigh         = (   0x0, 0x302D)
rOKTimeLow      = (   0x0, 0x302E)
rOKTimeHigh     = (   0x0, 0x302F)
rUID01          = (   0x0, 0x3030) # cartridge UID bytes 0 and 1
rUID23          = (   0x0, 0x3031) # cartridge UID bytes 2 and 3
rUID45          = (   0x0, 0x3032) # cartridge UID bytes 4 and 5
rUID67          = (   0x0, 0x3033) # cartridge UID bytes 6 and 7
rUID89          = (   0x0, 0x3034) # cartridge UID bytes 8 and 9
rUIDAB          = (   0x0, 0x3035) # cartridge UID bytes A and B
rUIDCD          = (   0x0, 0x3036) # cartridge UID bytes C and D
rUIDEF          = (   0x0, 0x3037) # cartridge UID bytes E and F
rCart01         = (   0x0, 0x3038) # cartridge part number bytes 0 and 1
rCart23         = (   0x0, 0x3039) # cartridge part number bytes 2 and 3
rCart45         = (   0x0, 0x303A) # cartridge part number bytes 4 and 5
rCartRev        = (   0x0, 0x303B) # cartridge revision level
rCartCurrent    = (   0x0, 0x303C) # cartridge nominal current
rCartStarts     = (   0x0, 0x3040) # cartridge total starts
rCartPilotTime  = (   0x0, 0x3041) # cartridge pilot arc time
rCartOK         = (   0x0, 0x3042) # cartridge total transfers
rCartOKTime     = (   0x0, 0x3043) # cartridge transfer time
rCartFault0     = (   0x0, 0x3044) # cartridge fault 0
rCartFault1     = (   0x0, 0x3045) # cartridge fault 1
rCartFault2     = (   0x0, 0x3046) # cartridge fault 2
rCartFault3     = (   0x0, 0x3047) # cartridge fault 3
rCartName01     = (   0x0, 0x3048) # cartridge name bytes 0 and 1
rCartName23     = (   0x0, 0x3049) # cartridge name bytes 2 and 3
rCartName45     = (   0x0, 0x304A) # cartridge name bytes 4 and 5
rCartName67     = (   0x0, 0x304B) # cartridge name bytes 6 and 7
rCartName89     = (   0x0, 0x304C) # cartridge name bytes 8 and 9
rCartNameAB     = (   0x0, 0x304D) # cartridge name bytes A and B

# write registers
rModeSet        = (0x2093, 0x3080)
rCurrentSet     = (0x2094, 0x3081)
rPressureSet    = (0x2096, 0x3082)
rRestart        = (   0x0, 0x308E) # quick restart command, write 0x0404 to this address
rRestartApp     = (   0x0, 0x308F) # quick restart approval, write 0x0618 to this address

# read coils
cLeadLengthLow  = (0x0808,    0x0)
cLeadLengthHigh = (0x0809,    0x0)
cStartSwitch    = (0x0810, 0x3100)
cMotionSwitch   = (0x0811, 0x3101)

# write coils
cGasTest        = (0x0832, 0x3180) # write 0xFF00 to start or 0x0000 to stop

machine = {'303831323838': [0, 'Powermax45'],
           '303831323233': [0, 'Powermax65/85/105'],
           '303831323531': [0, 'Powermax125'],
           '303831333335': [1, 'Powermax65/85/105 SYNC'],
           '303831323111': [0, 'Powermax Emulator']}

lLength = {'00': '15 ~ 25 ft (≤7.6 m)',
           '01': '35 ~ 50 ft (≤15 m)',
           '10': '75 ft (≤23 m)'}

sTorch = {'00': 'Hand torch with 7.6 m (25-foot) lead',
          '01': 'Hand torch with 15 m (50-foot) lead',
          '02': 'Hand torch with 23 m (75-foot) lead',
          '04': 'Machine torch with 4.6 m ~ 7.6 m (15-foot ~ 25-foot) lead',
          '05': 'Machine torch with 10.7 m ~ 15 m (35-foot ~ 50-foot) lead',
          '06': 'Machine torch with 23 m (75-foot) lead'}

sPPS = {'00': 'Powermax65 SYNC 200 V ~ 600 V CSA',
        '01': 'Powermax65 SYNC 380 V CCC / 400 V CE',
        '02': 'Powermax85 SYNC 200 V ~ 600 V CSA',
        '03': 'Powermax85 SYNC 380 V CCC / 400 V CE',
        '08': 'Powermax105 SYNC 200 V ~ 600 V CSA',
        '09': 'Powermax105 SYNC 230 V ~ 400 V CE',
        '0A':'Powermax105 SYNC 380 V CCC / 400 V CE'}

sCartridge = {'343238393336': 'Cut: 105 A cartridge',
              '343238393334': 'Cut: 85 A cartridge',
              '343238393330': 'Cut: 65 A cartridge',
              '343238393235': 'Cut: 45 A cartridge',
              '343238393236': 'FineCut: 45 A cartridge',
              '343238393339': 'Max Control gouge: 105 A cartridge',
              '343238393333': 'Max Control gouge: 65 A / 85 A cartridge',
              '343238393239': 'Max Control gouge: 45 A cartridge',
              '343238393338': 'Max Removal gouge: 105 A cartridge',
              '343238393332': 'Max Removal gouge: 65 A / 85 A cartridge',
              '000000000000': 'Cartridge communication failure or radio frequency error'}

sCartName = {'43204D454348000000000000': 'Standard Mechanized Cutting',
             '43204D464E43000000000000': 'FineCut Mechanized Cutting',
             '4720434E544C000000000000': 'Maximum Control Gouging',
             '4720524D564C000000000000': 'Maximum Removal Gouging',
             '432048414E44000000000000': 'Drag Hand Cutting',
             '432048464E43000000000000': 'FineCut Hand Cutting',
             '4320464C5553480000000000': 'FlushCut Cutting'}

class App(QWidget):
    def __init__(self):
        super().__init__()
        if not sMod:
            msg = '\npyserial module not available\n'\
                  '\nto install, open a terminal and enter:\n'\
                  '\nsudo apt-get install python3-serial\n'
            response = QMessageBox()
            response.setText(msg)
            response.exec_()
            raise SystemExit
        self.fg0 = '#ffee06'
        self.bg0 = '#16160e'
        self.bg1 = '#1d1d1d'
        self.bg2 = '#282828'
        self.disabled = 'gray'
        self.green = '#009900'
        self.rowHeight = 20
#FIXME.standalone - temporarily commented for standalone testing
        # self.iconPath = 'share/icons/hicolor/scalable/apps/linuxcnc_alt/linuxcncicon_plasma.svg'
        # appPath = os.path.realpath(os.path.dirname(sys.argv[0]))
        # self.iconBase = '/usr' if appPath == '/usr/bin' else appPath.replace('/bin', '/debian/extras/usr')
        # self.setWindowIcon(QIcon(os.path.join(self.iconBase, self.iconPath)))
        self.setWindowTitle('Powermax Communicator')
        self.pps = 0 # plasma power supply, 0=legacy, 1=SYNC
        self.createGridLayout()
        self.setStyleSheet(f'''
            QWidget {{color: {self.fg0}; background: {self.bg0}}}
            QLabel {{min-height: {self.rowHeight}; max-height: {self.rowHeight}}}
            QLabel#vLabel {{background: {self.bg1}; border-radius: 4; padding-right: 4}}
            QLabel#led {{background: {self.bg1}; border-radius: {self.rowHeight/2}; min-width: {self.rowHeight}; max-width: {self.rowHeight}}}
            QPushButton {{border: 1 solid {self.fg0}; border-radius: 4; height: {self.rowHeight-2}}}
            QPushButton#sPB {{font-size: 7pt}}
            QPushButton:pressed {{background: {self.bg1}}}
            QComboBox {{color: {self.fg0}; background-color: {self.bg0}; border: 1 solid {self.fg0}; border-radius: 4; height: {self.rowHeight-2}; padding-left: 50}}
            QComboBox::drop-down {{width: 0}}
            QComboBox QListView {{border: 4p solid {self.fg0}; border-radius: 0}}
            QComboBox QAbstractItemView {{text-align: right;border: 2px solid {self.fg0}; border-radius: 4}}
            QDoubleSpinBox {{border: 1 solid {self.fg0}; border-radius: 4; height: {self.rowHeight-2}}}
            QRadioButton::indicator {{border: 1px solid {self.fg0}; border-radius: 4; height: {self.rowHeight-2}; width: {self.rowHeight-2}}}
            QRadioButton::indicator:disabled {{color: {self.disabled}; border-color: {self.disabled}}}
            QRadioButton::indicator:checked {{background: {self.fg0}}}
            QRadioButton::indicator:checked:disabled {{background: {self.disabled}}}
            QDoubleSpinBox::up-button {{subcontrol-origin:padding; subcontrol-position:right; width: {self.rowHeight+2}; height: {self.rowHeight-4}}}
            QDoubleSpinBox::down-button {{subcontrol-origin:padding; subcontrol-position:left; width: {self.rowHeight+2}; height: {self.rowHeight-4}}}
            QMessageBox {{color: {self.fg0}; background-color: {self.bg0}}}
            ''')
#            QComboBox::drop-down {{subcontrol-origin: padding;  subcontrol-position: top right; width: 40px;border: 0px ;}}
        self.setLayout(self.grid)
        self.show()
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.timer = QTimer(self)
        self.portName.addItem('SELECT A PORT')
        for item in serial.tools.list_ports.comports():
            self.portName.addItem(item.device)
        self.portFile = None
        self.openPort = None
        self.pressureType = 'psi'
        self.minPressure = 0
        self.machineText = ['','','','','']
        self.close_connection()
        self.portName.activated.connect(self.port_changed)
        self.portScan.pressed.connect(self.scan_for_ports)
        self.local.toggled.connect(self.remote_mode_toggled)
        self.modeSet.currentIndexChanged.connect(lambda:self.change_value(self.modeSet, rModeSet[self.pps], 1))
        self.currentSet.valueChanged.connect(lambda:self.change_value(self.currentSet, rCurrentSet[self.pps], 64))
        self.pressureSet.valueChanged.connect(lambda:self.change_value(self.pressureSet, rPressureSet[self.pps], 128))
        self.gasTest.pressed.connect(self.gas_test_pressed)
        self.timer.timeout.connect(self.periodic)
        self.scan_for_ports()

    def periodic(self):
#FIXME.time - temp for timing
        rt=time.monotonic()
        if not os.path.exists(self.portFile): # or not self.connected:
            self.timer.stop()
            self.close_connection()
            self.clear_text()
            self.portName.clear()
            self.portName.addItem('SELECT A PORT')
            try:
                self.openPort.close()
            except:
                pass
            self.dialog_ok(
                        QMessageBox.Warning,\
                        'Error',\
                        '\nCommunications device lost.\n'\
                        '\nA Port Scan is required.\n')
        elif self.connected:
            # SYNC power supplies
            if self.pps:
                pass
            # legacy power supplies
            else:
                faultH, faultL = self.read_machine(rFault[self.pps], 1)
                if None not in [faultH, faultL]:
                    fault = int(f'{faultH}{faultL}', 16)
                    faultText = f'{fault:04d}'
                    if fault == 0:
                        self.faultValue.setText('')
                        self.faultName.setText('')
                    elif faultText in faultCode:
                        self.faultValue.setText(f'{faultText[0]}-{faultText[1:3]}-{faultText[3]}')
                        if fault == 210:
                            if float(self.currentMax.text()) > 110 and not self.pps:
                                # for 105/125 legacy power supplies only
                                self.faultName.setText(f'{faultCode[faultText][1]}')
                            else:
                                # all other power supplies
                                self.faultName.setText(f'{faultCode[faultText][0]}')
                        else:
                            self.faultName.setText(f'{faultCode[faultText]}')
                    else:
                        self.faultName.setText('UNKNOWN FAULT CODE')

                arcLH, arcLL, arcHH, arcHL = self.read_machine(rArcTimeLow[self.pps], 2)
                if None not in [arcLH, arcLL, arcHH, arcHL]:
                    arcL = int(arcLH + arcLL, 16)
                    arcH = int(arcHH + arcHL, 16)
                    m, s = divmod(arcL + arcH, 60)
                    h, m = divmod(m, 60)
                    self.arctimeValue.setText(f'{h:.0f}h {m:02.0f}m {s:02.0f}s')

                pressureAH, pressureAL = self.read_machine(rPressureGet[self.pps], 1)
                if None not in [pressureAH, pressureAL]:
                    pressure = int(pressureAH + pressureAL, 16) / 128
                    dp = 1 if self.pressureType == 'bar' else 0
                    self.actualPressure.setText(f'{pressure:.{dp}f}')

                switches = self.read_machine(cStartSwitch[self.pps], 2, coil=True)[0]
                if switches is not None:
                    switches = int(switches)
                    if 1 & switches:
                        self.startL.setStyleSheet(f'QLabel {{background: {self.green}}}')
                    else:
                        self.startL.setStyleSheet(f'QLabel {{background: {self.bg1}}}')
                    if 2 & switches:
                        self.motionL.setStyleSheet(f'QLabel {{background: {self.green}}}')
                    else:
                        self.motionL.setStyleSheet(f'QLabel {{background: {self.bg1}}}')
            self.show_machine_label()
        else:
            self.port_changed()
        #FIXME.time - temp for timing
        rt=time.monotonic()-rt
#        print(f'periodic loop  = {rt:.3f} seconds')

    def scan_for_ports(self):
        while not self.connected:
            self.local.setChecked(True)
            self.timer.stop()
            self.clear_text()
            try:
                self.openPort.close()
            except:
                pass
            self.portName.clear()
            self.portName.addItem('SELECT A PORT')
            for item in serial.tools.list_ports.comports():
                self.portName.addItem(item.device)
            self.local.setEnabled(False)
            self.remote.setEnabled(False)
            self.portName.setCurrentIndex( self.portName.count() - 1 )
            self.port_changed()

    def port_changed(self):
        self.close_connection()
        if self.portName.currentText() == 'SELECT A PORT':
            self.clear_text()
            return
        try:
            self.openPort.close()
        except:
            pass
        try:
            self.openPort = serial.Serial(
                    self.portName.currentText(),
                    baudrate = 19200,
                    bytesize = 8,
                    parity = 'E',
                    stopbits = 1,
                    timeout = 0.1
                    )
        except:
            self.dialog_ok(QMessageBox.Warning, 'Error', f'\nCould not open {self.portName.currentText()}\n')
            return
        self.local.setEnabled(True)
        self.remote.setEnabled(True)
        self.portFile = self.portName.currentText()
        self.identify_machine()
        self.get_limits()

    def identify_machine(self):
        txPacket = ':012B0E0401C1\r\n'
        errors = 0
        rxPacket = ''
        while not rxPacket:
            self.openPort.write(txPacket.encode())
            rxPacket = self.openPort.readline().decode()
            if not rxPacket:
                errors += 1
                if errors == 5:
                    rxPacket = 'Nope'
        if len(rxPacket) == 37 and self.get_lrc(rxPacket[1:-4]) == rxPacket[-4:-2]:
            id = rxPacket[21:-4]
            if id in machine:
                self.pps, self.machineText[0] = machine[id]
            else:
                self.pps = 0
                self.machineText[0] = 'Unknown Plasma Power Supply'
            if self.pps:
                pps = self.read_machine(rTorchPPS[self.pps], 1)[1]
                if pps is not None:
                    self.self.machineText[0] = sPPS[pps]
                else:
                    self.self.machineText[0] = 'Unknown SYNC Plasma Power Supply'

            length = self.read_machine(cLeadLengthLow[self.pps], 2, coil=True)[0]
            if length is not None:
                length = f'{int(length):02b}'
                self.machineText[1] = f'torch lead = {lLength[length]}'

            self.show_machine_label()
            self.connected = True
            self.timer.start(500)
        else:
            self.dialog_ok(QMessageBox.Warning, 'Error', f'\nCould not identify a plasma power supply on {self.portName.currentText()}\n')

    def get_limits(self):
        minCH, minCL, \
        maxCH, maxCL, \
        void5, void6, \
        minPH, minPL, \
        maxPH, maxPL = self.read_machine(rCurrentMin[self.pps], 5)
        if None not in [minCH, minCL, maxCH, maxCL]:
            minC = int(minCH + minCL , 16) // 64
            maxC = int(maxCH + maxCL , 16) // 64
            self.currentSet.setRange(minC, maxC)
            self.currentMin.setText(f'{minC}')
            self.currentMax.setText(f'{maxC}')
        if None not in [minPH, minPL, maxPH, maxPL]:
            self.minPressure = int(minPH + minPL, 16) // 128
            self.maxPressure = int(maxPH + maxPL, 16) // 128
            self.pressureSet.setRange((0), self.maxPressure)
            self.pressureMin.setText(f'{self.minPressure}')
            self.pressureMax.setText(f'{self.maxPressure}')

    def remote_mode_toggled(self):
        rt=time.monotonic()
        if self.pps:
            local = '000000000000'
            numRegs = 3
        else:
            local = '0000000000000000'
            numRegs = 4
        if self.local.isChecked():
            if not self.write_register(regWriteMult, rModeSet[self.pps], local, numRegs):
                return
            self.portName.setEnabled = True
        else:
            if self.currentSet.value() == 0:
                result = self.dialog_ok(
                        QMessageBox.Warning,\
                        'Error',\
                        '\nA value is required for Current.\n')
                if result:
                    self.local.setEnabled(True)
                    return
            self.portName.setEnabled = False
            mode = f'{self.modeSet.currentIndex() + 1:04X}'
            current = f'{int(self.currentSet.value() * 64):04X}'
            pressure = f'{int(self.pressureSet.value() * 128):04X}'
            if self.pps:
                remote = f'{mode}{current}{pressure}'
            else:
                remote = f'{mode}{current}0000{pressure}'
            if not self.write_register(regWriteMult, rModeSet[self.pps], remote, numRegs):
                return
            self.get_limits()
        rt=time.monotonic()-rt
        print(f'remote_mode_toggled = {rt:.3f} seconds')

    def change_value(self, widget, reg, multiplier):
        rt=time.monotonic()
        if not self.connected:
            return
        if reg == rModeSet[self.pps]:
            mode = self.modeSet.currentIndex() + 1
            self.pressureSet.setValue(0)
            data = f'{mode:04X}'
        elif reg == rPressureSet[self.pps]:
            if self.pressureType == 'bar':
                if widget.value() == 0.1:
                    widget.setValue(self.minPressure)
                elif widget.value() == self.minPressure - 0.1:
                    widget.setValue(0)
            else:
                if widget.value() == 1:
                    widget.setValue(self.minPressure)
                elif widget.value() == self.minPressure - 1:
                    widget.setValue(0)
            data = (f'{int(widget.value() * multiplier):04X}').upper()
        elif reg == rCurrentSet[self.pps]:
            data = (f'{int(widget.value() * multiplier):04X}').upper()
        if self.remote.isChecked():
            if self.write_register(regWrite, reg , data):
                self.get_limits()
        rt=time.monotonic()-rt
        print(f'change_value = {rt:.3f} seconds')

    def gas_test_pressed(self):
        if self.gasTest.palette().color(QPalette.Background).name() == self.bg0:
            if self.write_register(coilWrite, cGasTest[self.pps], 'FF00'):
                self.gasTest.setStyleSheet(f'QPushButton {{background: {self.green}}} ')
        else:
            if self.write_register(coilWrite, cGasTest[self.pps], '0000'):
                self.gasTest.setStyleSheet(f'QPushbutton {{background: {self.bg0}}}')

    def get_lrc(self, data):
        lrc = 0
        for i in range(0, len(data), 2):
            try:
                a, b = data[i:i+2]
                lrc = (lrc + int(a + b, 16)) & 255
            except:
                print('error getting LRC')
                return '00'
        lrc = (f'{(((lrc ^ 255) + 1) & 255):02X}').upper()
        return lrc

    def write_register(self, func, reg, data, numRegs=1):
#        print(f'write_register(self, {func}, {reg}, {data}, {numRegs})') # TEMP DEBUG PRINT
        if func == coilWrite:
            tx = f'{address:02X}{func:02X}{reg:04X}{data}'
            rx = f'{address:02X}{func:02X}{reg:04X}{data}'
        elif func == regWrite:
            tx = f'{address:02X}{func:02X}{reg:04X}{data}'
            rx = f'{address:02X}{func:02X}{reg:04X}{data}'
        elif func == regWriteMult:
            tx = f'{address:02X}{func:02X}{reg:04X}{numRegs:04X}{numRegs * 2:02X}{data}'
            rx = f'{address:02X}{func:02X}{reg:04X}{numRegs:04X}'
        txPacket = f':{tx}{self.get_lrc(tx)}\r\n'
        rxValid = f':{rx}{self.get_lrc(rx)}\r\n'
        errors = 0
        while 1:
            try:
                rxPacket = ''
                self.openPort.write(txPacket.encode())
                rxPacket = self.openPort.readline().decode()
#FIXME.sync - temporary output for SYNC addition
                mode = 'Remote' if self.remote.isChecked() else ' Local'
                self.tView.append(f"          write_register {mode} TX={ascii(txPacket)} RX={ascii(rxPacket)}")
                self.tView.moveCursor(QTextCursor.End)
                self.logFile.write(f"          write_register {mode} TX={ascii(txPacket)} RX={ascii(rxPacket)}\n")
                self.logFile.flush()
            except Exception as e:
                self.local.setChecked(True)
                self.dialog_ok(QMessageBox.Warning, 'Error', f'\nError while writing to plasma unit.\n\n{e}\n')
                return False
            if rxPacket == rxValid:
#                print(f"good: tx={ascii(txPacket)}   in={ascii(rxPacket)}   valid={ascii(rxValid)}") # TEMP DEBUG PRINT
                break
            elif rxPacket:
#                print(f" bad: tx={ascii(txPacket)}   in={ascii(rxPacket)}   valid={ascii(rxValid)}") # TEMP DEBUG PRINT
                errors += 1
                if errors == 3:
                    self.local.setChecked(True)
                    self.dialog_ok(QMessageBox.Warning, 'Error', '\nInvalid reply while writing to plasma unit.\n')
                    return False
            else:
                #print(f"none: tx={ascii(txPacket)}   in={ascii(rxPacket)}   valid={ascii(rxValid)}") # TEMP DEBUG PRINT
                errors += 1
                if errors == 3:
                    self.local.setChecked(True)
                    self.dialog_ok(QMessageBox.Warning, 'Error', '\nNo reply while writing to plasma unit.\n\nCheck connections and retry when ready.\n')
                    return False
        return True

    def read_machine(self, reg, numRegs, coil=False, custom=False):
#        print(f'reg={reg}   mumRegs={numRegs}   coil={coil}   custom={custom}') # TEMP DEBUG PRINT
        func = coilRead if coil else regRead
        data = f'{address:02X}{func:02X}{reg:04X}{numRegs:04X}'
        lrc =self.get_lrc(data)
        txPacket = f':{data}{lrc}\r\n'
        rxPacket = ''
        try:
            self.openPort.write(txPacket.encode())
            rxPacket = self.openPort.readline().decode()
        except:
            self.close_connection()
            self.dialog_ok(QMessageBox.Warning, 'Error', '\nCould not open port.\n\nCheck connections and retry when ready.\n')
            return [None] * numRegs * 2
        if not rxPacket:
            self.close_connection()
            self.dialog_ok(QMessageBox.Warning, 'Error', '\nNo reply while reading from plasma unit.\n\nCheck connections and retry when ready.\n')
            return [None] * numRegs * 2
#        print(f'000={rxPacket[1:-2].strip()}> from:{ascii(rxPacket)}>')
        if rxPacket[0] != ':' or rxPacket[-2:] != '\r\n':
#        if not int(rxPacket[1:-2].strip(), 16) >= 0:
            self.close_connection()
            self.dialog_ok(QMessageBox.Warning, 'Error', f'\nInvalid data returned from read_machine {reg:04X}\n\nTX: {ascii(txPacket)}\nRX: {ascii(rxPacket)}')
            return [None] * numRegs *2
        numBytes = int(rxPacket[5:7], 16)
        data = rxPacket[7:-4]
        lrc = rxPacket[-4:-2]
        if lrc != self.get_lrc(rxPacket[1:-4]):
            self.dialog_ok(QMessageBox.Warning, 'Error', f'\nIncorrect LRC from read_machine {reg:04X}\n\nreceived: {ascii(self.get_lrc(rxPacket[1:-4]))}\nrequired: {ascii(lrc)}')
            return [None] * numRegs * 2
        try:
            result = WRAP(data, len(data) // numBytes)
#        print(f'result={result}  numBytes={numBytes}  data={data}  lrc={lrc}  rxPacket={ascii(rxPacket)}  txPacket={ascii(txPacket)}') # TEMP DEBUG PRINT
            return result
        except:
            print('OMG, something bad happened...')
        return [None] * numRegs * 2

    def close_connection(self):
        self.connected = False
        self.local.setChecked(True)
        self.local.setEnabled(False)
        self.remote.setEnabled(False)

    def clear_text(self):
        if self.pps:
            self.machineLabel.setText('\n\n\n')
        else:
            self.machineLabel.setText('\n')
        self.modeValue.setText('')
        self.currentValue.setText('')
        self.pressureValue.setText('')
        self.faultValue.setText('')
        self.currentMin.setText('')
        self.pressureMin.setText('')
        self.faultName.setText('')
        self.currentMax.setText('')
        self.pressureMax.setText('')
        self.arctimeValue.setText('')
        self.modeSet.setCurrentIndex(0)
        self.currentSet.setValue(40)
        self.pressureSet.setValue(0)

    def show_machine_label(self):
        text = f'{self.machineText[0]}   {self.machineText[1]}'
        for n in range(2, len(self.machineText)):
            if self.machineText[n]:
                text += f'\n{self.machineText[n]}'
        self.machineLabel.setText(text)

    def dialog_ok(self,icon,title,text):
        response = QMessageBox()
        response.setIcon(icon)
#FIXME.standalone - temporarily commented for standalone testing
        # response.setWindowIcon(QIcon(os.path.join(self.iconBase, self.iconPath)))
        response.setWindowTitle(title)
        response.setText(text);
        response.exec_()
        return response

    def createGridLayout(self):
        row = 0
        self.grid = QGridLayout()
        self.portScan = QPushButton('PORT SCAN')
        self.grid.addWidget(self.portScan,row,0)
        self.portName = QComboBox()
        self.portName.setStyleSheet('QComboBox {width: 240}')
        self.grid.addWidget(self.portName,row,1,1,2)
        pmxControl = QHBoxLayout()
        self.grid.addLayout(pmxControl,row,3,1,2)
        self.local = QRadioButton('LOCAL')
        self.local.setChecked(True)
        self.local.setEnabled(False)
        pmxControl.addWidget(self.local)#,0, Qt.AlignVCenter)
        cL = QLabel("POWERMAX CONTROL")
        pmxControl.addWidget(cL)#,1,Qt.AlignRight)
        self.remote = QRadioButton('REMOTE')
        self.remote.setLayoutDirection(Qt.RightToLeft)
        self.remote.setEnabled(False)
        pmxControl.addWidget(self.remote)#,2, Qt.AlignVCenter)
        row += 1
        self.machineLabel = QLabel(objectName='vLabel')
        self.machineLabel.setAlignment(Qt.AlignCenter| Qt.AlignVCenter)
        self.grid.addWidget(self.machineLabel,row,0,1,5)
        row += 1
        self.minLabel = QLabel('MIN.')
        self.minLabel.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.minLabel,row,1)
        self.maxLabel = QLabel('MAX.')
        self.maxLabel.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.maxLabel,row,2)
        self.valueLabel = QLabel('VALUE')
        self.valueLabel.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.valueLabel,row,3)
        self.setLabel = QLabel('SET TO')
        self.setLabel.setAlignment(Qt.AlignCenter| Qt.AlignVCenter)
        self.grid.addWidget(self.setLabel,row,4)
        row += 1
        self.modeLabel = QLabel('MODE')
        self.modeLabel.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.modeLabel,row,0)
        self.modeValue = QLabel('0', objectName='vLabel')
        self.modeValue.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.modeValue,row,3)
        self.modeSet = QComboBox()
        self.modeSet.addItems(['NORMAL','CPA','GOUGE'])
        self.modeSet.setCurrentIndex(0)
        self.grid.addWidget(self.modeSet,row,4)
        row += 1
        self.currentLabel = QLabel('CURRENT')
        self.currentLabel.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.currentLabel,row,0)
        self.currentMin = QLabel('0', objectName='vLabel')
        self.currentMin.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.currentMin,row,1)
        self.currentMax = QLabel('0', objectName='vLabel')
        self.currentMax.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.currentMax,row,2)
        self.currentValue = QLabel('0', objectName='vLabel')
        self.currentValue.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.currentValue,row,3)
        self.currentSet = QDoubleSpinBox()
        self.currentSet.setMaximum(125)
        self.currentSet.setWrapping(True)
        self.currentSet.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.currentSet.setDecimals(0)
        self.currentSet.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.grid.addWidget(self.currentSet,row,4)
        row += 1
        self.pressureLabel = QLabel('PRESSURE')
        self.pressureLabel.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.pressureLabel,row,0)
        self.pressureMin = QLabel('0', objectName='vLabel')
        self.pressureMin.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.pressureMin,row,1)
        self.pressureMax = QLabel('0', objectName='vLabel')
        self.pressureMax.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.pressureMax,row,2)
        self.pressureValue = QLabel('0', objectName='vLabel')
        self.pressureValue.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.pressureValue,row,3)
        self.pressureSet = QDoubleSpinBox()
        self.pressureSet.setMaximum(125)
        self.pressureSet.setWrapping(True)
        self.pressureSet.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.pressureSet.setDecimals(0)
        self.pressureSet.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.grid.addWidget(self.pressureSet,row,4)
        row += 1
        row += 1
        self.faultLabel = QLabel('FAULT')
        self.faultLabel.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.faultLabel,row,0)
        self.faultValue = QLabel('0', objectName='vLabel')
        self.faultValue.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.faultValue,row,1)
        self.faultName = QLabel('', objectName='vLabel')
        self.faultName.setAlignment(Qt.AlignLeft| Qt.AlignVCenter)
        self.grid.addWidget(self.faultName,row,2,1,2)
        row += 1
        actualPressure = QLabel('PRESSURE AT VALVE')
        actualPressure.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(actualPressure, row, 0)
        self.actualPressure = QLabel('', objectName='vLabel')
        self.actualPressure.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.actualPressure, row, 1)
        self.gasTest = QPushButton('GAS TEST')
        self.grid.addWidget(self.gasTest,row,2)
        row += 1
        self.arctimeLabel = QLabel('ARC ON TIME')
        self.arctimeLabel.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.arctimeLabel,row,0)
        self.arctimeValue = QLabel('0', objectName='vLabel')
        self.arctimeValue.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(self.arctimeValue,row,1)
        row += 1
        startL = QLabel('ARC ON')
        startL.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(startL,row, 0)
        self.startL = QLabel(objectName='led')
        self.grid.addWidget(self.startL,row,1)
        row += 1
        motionL = QLabel('ARC OK')
        motionL.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.grid.addWidget(motionL, row, 0)
        self.motionL = QLabel(objectName='led')
        self.grid.addWidget(self.motionL,row,1)


        self.clear_text()

#FIXME.sync - start temporary stuff for SYNC addition - may keep the custom code and gas test ???
        l0 = QLabel('REGISTERS')
        l0.setAlignment(Qt.AlignHCenter|Qt.AlignBottom)
        t0 = QPushButton('SET MODE=2', objectName='sPB')
        t1 = QPushButton('SET 45A', objectName='sPB')
        t2 = QPushButton('SET MODE=1 + 46A', objectName='sPB')
#        t3 = QPushButton('GET FAULT', objectName='sPB')
        t3 = QPushButton('GET PRESSURE', objectName='sPB')
        t4 = QPushButton('GET SET REGISTERS', objectName='sPB')
        l1 = QLabel('COILS')
        l1.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        t5 = QPushButton('SET GAS TEST ON', objectName='sPB')
        t6 = QPushButton('SET GAS TEST OFF', objectName='sPB')
        t7 = QPushButton('GET START SW', objectName='sPB')
        t8 = QPushButton('GET MOTION SW', objectName='sPB')
        t9 = QPushButton('GET START + MOTION SW', objectName='sPB')
        l2 = QLabel('CUSTOM DATA ENTRY')
        l2.setAlignment(Qt.AlignHCenter|Qt.AlignBottom)
        l3 = QLabel(':01 at start and LRC at end are auto generated, spaces are auto removed. Press `Return` to send')
        l3.setAlignment(Qt.AlignCenter)
        self.c0 = QLineEdit()
        self.c0.setInputMask('>hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
        self.c0.setAlignment(Qt.AlignCenter)
        self.c0.setStyleSheet(f'QLineEdit {{background: {self.bg2}; border: 1px solid {self.fg0}; border-radius: 4px; height: 20px; font: 7 pt courier}}')
        self.tView = QTextEdit()
        self.tView.setFixedHeight(180)
        row += 1
        row += 1
        self.grid.addWidget(l0,row,2)
        row += 1
        self.grid.addWidget(t0,row,0)
        self.grid.addWidget(t1,row,1)
        self.grid.addWidget(t2,row,2)
        self.grid.addWidget(t3,row,3)
        self.grid.addWidget(t4,row,4)
        row += 1
        row += 1
        self.grid.addWidget(l1,row,2)
        row += 1
        self.grid.addWidget(t5,row,0)
        self.grid.addWidget(t6,row,1)
        self.grid.addWidget(t7,row,2)
        self.grid.addWidget(t8,row,3)
        self.grid.addWidget(t9,row,4)
        row += 1
        row += 1
        self.grid.addWidget(l2,row,1,1,3)
        row += 1
        self.grid.addWidget(self.c0,row,0,1,5)
        row += 1
        self.grid.addWidget(l3,row,0,1,5)
        row += 1
        self.grid.addWidget(self.tView,row,0,1,5)
        self.tView.setStyleSheet(f'''
            QTextEdit {{border: 1 solid {self.fg0}; border-radius: 4; font: 7 pt courier; margin: 2px}}
            QScrollBar:vertical {{background: {self.bg2}; border: 0px; border-radius: 4px; margin: 0px; width: 20px }}
            QScrollBar::handle:vertical {{background: {self.fg0}; border: 2px solid {self.fg0}; border-radius: 4px; margin: 2px; min-height: 40px }}
            QScrollBar::add-line:vertical {{height: 0px }}
            QScrollBar::sub-line:vertical {{height: 0px }}
            ''')
        t0.clicked.connect(lambda:self.t0_clicked(t0.text().replace('\n','')))
        t1.clicked.connect(lambda:self.t1_clicked(t1.text().replace('\n','')))
        t2.clicked.connect(lambda:self.t2_clicked(t2.text().replace('\n','')))
        t3.clicked.connect(lambda:self.t3_clicked(t3.text().replace('\n','')))
        t4.clicked.connect(lambda:self.t4_clicked(t4.text().replace('\n','')))
        t5.clicked.connect(lambda:self.t5_clicked(t5.text().replace('\n','')))
        t6.clicked.connect(lambda:self.t6_clicked(t6.text().replace('\n','')))
        t7.clicked.connect(lambda:self.t7_clicked(t7.text().replace('\n','')))
        t8.clicked.connect(lambda:self.t8_clicked(t8.text().replace('\n','')))
        t9.clicked.connect(lambda:self.t9_clicked(t9.text().replace('\n','')))
        self.c0.returnPressed.connect(self.c0_entered)
        logFile = os.path.join(os.path.expanduser('~'), 'Downloads', f"pmx485_log_{time.strftime('%y-%m-%d_%H-%M-%S')}.txt")
        self.logFile = open(logFile, 'w')
        self.logFile.write(f"\nlog started on {time.strftime('%y-%m-%d')} at {time.strftime('%H-%M-%S')}\n\n")
        self.logFile.flush()

        for r in range(row + 1):
            self.grid.setRowMinimumHeight(r, self.rowHeight)
            self.grid.setRowStretch(r, 1)
        for c in range(5):
            self.grid.setColumnMinimumWidth(c, 154)
            self.grid.setColumnStretch(c, 1)

    def t0_clicked(self, text):
        self.t_write(text, ':010620930002') # write mode 2

    def t1_clicked(self, text):
        self.t_write(text, ':011020940001020B40') # write 45A

    def t2_clicked(self, text):
        self.t_write(text, ':0110209300020400010B80') # write mode 1 and 46A

    def t3_clicked(self, text):
#        self.t_write(text, ':010420980001') # read 1 fault
        self.t_write(text, ':0104204C0001') # read actual pressure

    def t4_clicked(self, text):
        self.t_write(text, ':010420930004') # read set registers mode, current, void, and pressure

    def t5_clicked(self, text):
        self.t_write(text, ':01050832FF00') # gas test on

    def t6_clicked(self, text):
        self.t_write(text, ':010508320000') # gas test off

    def t7_clicked(self, text):
        self.t_write(text, ':010108100001') # read start switch

    def t8_clicked(self, text):
        self.t_write(text, ':010108110001') # read motion switch

    def t9_clicked(self, text):
        self.t_write(text, ':010108100002') # read start switch and motion switch

    def c0_entered(self):
        text = self.c0.text() if self.c0.text()[:3] == ':01' else f":01{self.c0.text()}"
        self.t_write('Custom data               ', text) # custom data

    def t_write(self, button, data):
        try:
            if not self.openPort:
                self.tView.append('Port not selected')
                self.tView.moveCursor(QTextCursor.End)
                return
            if not self.openPort.isOpen():
                self.tView.append('Port not open', self.openPort.port())
                self.tView.moveCursor(QTextCursor.End)
                return
            txPacket = f"{data}{self.get_lrc(data[1:])}\r\n"
            errors = 0
            rxPacket = ''
            while not rxPacket:
                self.openPort.write(txPacket.encode())
                rxPacket = self.openPort.readline().decode()
                if not rxPacket:
                    errors += 1
                    if errors == 5:
                        rxPacket = 'no data recieved'
            mode = 'Remote' if self.remote.isChecked() else ' Local'
            self.tView.append(f"{button:>24} {mode} TX={ascii(txPacket)} RX={ascii(rxPacket)}")
            self.tView.moveCursor(QTextCursor.End)
            self.logFile.write(f"{button:>24} {mode} TX={ascii(txPacket)} RX={ascii(rxPacket)}\n")
            self.logFile.flush()
        except Exception as e:
            print(f"NO COMMS:\n{e}")
#FIXME.sync - end temporary stuff for SYNC addition - may keep the custom code???

    def shut_down(self):
        if self.remote.isChecked():
            if self.pps:
                local = '000000000000'
                numRegs = 3
            else:
                local = '0000000000000000'
                numRegs = 4
            self.write_register(regWriteMult, rModeSet[self.pps], local, numRegs)
#FIXME.sync - temporary for SYNC addition
        self.logFile.close()

faultCode = {
             '0000': '',
             '0110': 'Remote controller mode invalid',
             '0111': 'Remote controller current invalid',
             '0112': 'Remote controller pressure invalid',
             '0120': 'Low input gas pressure',
             '0121': 'Output gas pressure low',
             '0122': 'Output gas pressure high',
             '0123': 'Output gas pressure unstable',
             '0130': 'AC input power unstable',
             '0140': 'cartridge installation problem',
             '0141': 'cartridge is not recognized',
             '0199': 'Power board hardware protection',
             '0200': 'Low gas pressure',
             '0210': ('Gas flow lost while cutting', 'Excessive arc voltage'),
             '0220': 'No gas input',
             '0300': 'Torch stuck open',
             '0301': 'Torch stuck closed',
             '0320': 'End of consumable life',
             '0321': 'end-of-life cartridge installed',
             '0400': 'PFC/Boost IGBT module under temperature',
             '0401': 'PFC/Boost IGBT module over temperature',
             '0402': 'Inverter IGBT module under temperature',
             '0403': 'Inverter IGBT module over temperature',
             '0500': 'Retaining cap off',
             '0501': 'torch-lock switch is yellow',
             '0502': 'torch-lock switch is green but the torch is not ready',
             '0503': 'system is reading',
             '0510': 'Start/trigger signal on at power up',
             '0520': 'Torch not connected',
             '0600': 'AC input voltage phase loss',
             '0601': 'AC input voltage too low',
             '0602': 'AC input voltage too high',
             '0610': 'AC input unstable',
             '0980': 'Internal communication failure',
             '0981': 'communication failure between cartridge and torch',
             '0982': 'communication failure between torch and plasma power supply',
             '0990': 'System hardware fault',
             '1000': 'Digital signal processor fault',
             '1100': 'A/D converter fault',
             '1200': 'I/O fault',
             '1300': 'A flash memory fault occurred',
             '2000': 'A/D converter value out of range',
             '2010': 'Auxiliary switch disconnected',
             '2100': 'Inverter module temp sensor open',
             '2101': 'Inverter module temp sensor shorted',
             '2110': 'Pressure sensor is open',
             '2111': 'Pressure sensor is shorted',
             '2200': 'DSP does not recognize the torch',
             '3000': 'Bus voltage fault',
             '3100': 'Fan speed fault',
             '3101': 'Fan fault',
             '3110': 'PFC module temperature sensor open',
             '3111': 'PFC module temperature sensor shorted',
             '3112': 'PFC module temperature sensor circuit fault',
             '3200': 'Fill valve',
             '3201': 'Dump valve',
             '3202': 'Valve ID',
             '3203': 'Electronic regulator is disconnected',
             '3410': 'Drive fault',
             '3420': '5 or 24 VDC fault',
             '3421': '18 VDC fault',
             '3430': 'Inverter capacitors unbalanced',
             '3441': 'PFC over current',
             '3511': 'Inverter saturation fault',
             '3520': 'Inverter shoot-through fault',
             '3600': 'Power board fault',
             '3700': 'Internal serial communications fault',
            }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.aboutToQuit.connect(ex.shut_down)
    sys.exit(app.exec_())
