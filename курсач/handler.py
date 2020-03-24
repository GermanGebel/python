class Handler: 
    def __init__(self):
        pass 

    @staticmethod
    def getTempFromRooms(sock,tempDict):
        command = "YT0\r\n"
        try:
            sock.send(command)
            response = sock.recv(88)
            answer = response.decode('utf-8')
            return answer.split('#')[1:6]
        except Exception: 
            return None

    @staticmethod
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
                
    @staticmethod
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
