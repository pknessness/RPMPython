#!env/bin/python
from datetime import datetime, timezone
import serial.tools.list_ports
from PyQt6.QtWidgets import *
import serial
import time, platform, threading
from datetime import datetime, timezone
# termiosBullshit = 1

# if(termiosBullshit):
#     import termios

#     port = '/dev/ttyACM0'
#     f = open(port)
#     attrs = termios.tcgetattr(f)
#     attrs[2] = attrs[2] & ~termios.HUPCL
#     termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
#     f.close()

ports = []

status = 0

filename = "NO_PROFILE"

def newFile():
    global filename
    now = datetime.now()
    filename = "logs/log_"+now.strftime("%d-%m-%Y_%H_%M_%S")
    #f = open(filename + ".csv", "w").close()
    
def writeFile(text):
    f = open(filename + ".csv", "a")
    f.write(text)

def get_root():
    text_file = open("index.html", "r")
 
    #read whole file to a string
    data = text_file.read()
    
    #close file
    text_file.close()
    #return HTMLResponse(data,status_code=200)
    
def scan():
    global ports
    ports = []
    for port in serial.tools.list_ports.comports():
        
        try:
            s = serial.Serial(port.name)
            ports.append({"port": port.name, "device" : s.portstr})
        except:
            ports.append({"port": port.name, "device" : "NA"})
            pass
    print(ports)
    return ports
    
def serialInit(block = None):
    ser = serial.Serial(dsrdtr=None)
    #ser.port = "/dev/"+ port
    
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    
    #ser.timeout = None          #block read
    #ser.timeout = 1            #non-block read
    #ser.timeout = 2              #timeout block read
    ser.timeout = block
    
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = None       #disable hardware (DSR/DTR) flow control
    
    ser.setDTR(False)
    
    #ser.writeTimeout = 2     #timeout for write
    if(len(ports) == 0):
        scan()
    try:
        for port in ports:
            if(platform.system() == "Windows" and port['device'] == 'NA'):
                continue
            if(platform.system() == "Windows"):
                ser.port = port['port']
            else:
                ser.port = "/dev/"+ port['port']
            #print("initalized ser",ser)
            ser.open()
    except:
        scan()
        try:
            for port in ports:
                if(platform.system() == "Windows" and port['device'] == 'NA'):
                    continue
                if(platform.system() == "Windows"):
                    ser.port = port['port']
                else:
                    ser.port = "/dev/"+ port['port']
                #print("initalized ser",ser)
                ser.open()
        except Exception as e:
            
            return e
    return ser
    
def writeRead(writeString):
    ser = serialInit(1)
    
    response = None
    
    if(isinstance(ser,Exception)): return ser
    
    try:
        print(f"Attempting write {writeString} from Arduino {ser}:")
        ser.write(writeString.encode('utf-8'))
    except Exception as e:
        return e
    time.sleep(1)
    try:
        print("Attempting read from Arduino:")
        by = ser.inWaiting()
        response = ser.read(by).decode('utf-8')
        print(by, response)
    except Exception as e:
        return e
    
    ser.close()
    return response
    
def start(): 
    global status
    if(status == 0):
        threading.Timer(0.1, request_data).start()
    else:
        return
    status = 1
    response = writeRead("a")
    newFile()
    writeFile("accel_x,accel_y,accel_z,encoder_a,encoder_b, t\n")
    if(isinstance(response,Exception)): return response
    return response

def stop(): 
    response = writeRead("r")
    filename = "NO_PROFILE"
    if(isinstance(response,Exception)): return response
    return response
    
def request_data(): 
    response = writeRead("d")
    if(isinstance(response,Exception)):
        writeFile(str(response)+"\n")
        return response
    else:
        text = response.replace("+","").replace("#","").replace("==","=")
        values = text.split("=")
        writeFile(f"{values[0]},{values[1]},{values[2]},{values[3]},{values[4]},{datetime.utcnow()}\n")
    return response

# async def commands(info: Request):
#     data = await info.json()
#     if(data['command'] == "START"):
#         status = start()
#         return JSONResponse({
#             "command": "START",
#             "status": str(status)
#         })
#     if(data['command'] == "UPLOAD"):
#         status = upload(data['data'])
#         return JSONResponse({
#             "command": "UPLOAD",
#             "status": str(status)
#         })
#     if(data['command'] == "STOP"):
#         status = stop()
#         return JSONResponse({
#             "command": "STOP",
#             "status": str(status)
#         })
#     if(data['command'] == "REQUEST_DATA"):
#         status = request_data()
#         return JSONResponse({
#             "command": "REQUEST_DATA",
#             "status": str(status)
#         })
            
        
#     return JSONResponse({
#         "command": "UNKNOWN",
#         "status": "UNKNOWN"
#     })
    

if __name__ == "__main__":
    #uvicorn.run(app, host="127.0.0.1", port=8000)
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    
    startB = QPushButton('Start')
    stopB = QPushButton('Stop')
    
    startB.clicked.connect(start)
    stopB.clicked.connect(stop)
    
    layout.addWidget(startB)
    layout.addWidget(stopB)
    window.setLayout(layout)
    window.show()
    app.exec()
    


