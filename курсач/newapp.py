import bluetooth
import time
import threading
target_name = "SmartHome"
addr = "AB:68:32:57:34:02"
target_address = addr
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((addr, port))
# sock.send("YT0\r\n")
# response = sock.recv(88)
# answer = response.decode('utf-8')
# print(answer.split('#')[1:6])

def controlPower():
    pass
def getTempFromRooms(sock,tempDict):
    command = "YT0\r\n"
    try:
        sock.send(command)
        response = sock.recv(88)
        answer = response.decode('utf-8')
        return answer.split('#')[1:6]
    except Exception: 
        return None

def strControl(room, power):
    if power<0:
        if power%10==0:
            return 'XC{}q\r\n'.format(room)
        else:
            return 'XC{}{}\r\n'.format(room,abs(power))
    else:
        if power%10==0:
            return 'XH{}q\r\n'.format(room)
        else:
            return 'XH{}{}\r\n'.format(room,abs(power))

def funControl(t_old, t_now, t_need, power):#return UP DOWN STOP
    neuron_h = 1 if t_now - t_old>0 else 0
    neuron_c = 1 if t_now - t_old<0 else 0

    neuron_dt_h = 1 if t_need - t_now>=0.5 else 0
    neuron_dt_c = 1 if t_need - t_now<=-0.1 else 0

    neuron_up = 1 if neuron_dt_h-neuron_h>=1 else 0
    neuron_down = 1 if neuron_dt_c-neuron_c>=1 else 0
    neuron_stop = 1 if neuron_h+neuron_c-neuron_up-neuron_down>=1 else 0
    # print('{},{},{},{}'.format(neuron_h,neuron_c,neuron_dt_h,neuron_dt_c))
    # print('{},{},{}'.format(neuron_up, neuron_stop , neuron_down))
    if neuron_up>0:
        if power+1>10:
            return 10
        else:
            return power+1
    elif neuron_down>0:
        if power-1<-10:
            return -10
        else:
            return power-1
    elif neuron_stop>0:
        return power
    return power
temp_need = 28
temp_old = 20
temp_now = 20
power = 0
for i in range(1000):
    sock.send("YT0\r\n")
    response = sock.recv(88)
    answer = response.decode('utf-8')
    
    a = answer.split('#')[1]
    print("answer1 = {}".format(a))
    try:
        float(a)
        temp_old = temp_now
        temp_now = float(a)
    except:
        temp_old = temp_now
    if i>2:
        power_new = funControl(temp_old,temp_now,temp_need,power)
        print('newpower = {}'.format(power_new))
        if power != power_new:
            power = power_new
            control = strControl(1,power)
            print('Control = {}'.format(control))
            sock.send(control)      
            response = sock.recv(88)
            answer = response.decode('utf-8')
            print("answer2 = {}".format(answer))
    print("t_old={}, t_now = {}, power = {}".format(temp_old,temp_now, power))
    time.sleep(1)
sock.close()