# from simple_pid import PID

# # H = [i for i in range(65) if i%6==0]
# # C = [i for i in range(0,-32,-1) if i%3==0]
# # print("H:{},C:{}".format(H,C))
# # assume we have a system we want to control in controlled_system
# for i in range(10):
#     v = int(input())
#     pid = PID(0.5, 0.01, 10, setpoint=23)
#     control = pid(v)+23
#     print(control)

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

def funControl(t_old, t_now, t_need):#return UP DOWN STOP
    neuron_h = 1 if t_now - t_old>=0.3 else 0
    neuron_c = 1 if t_now - t_old<=-0.3 else 0

    neuron_dt_h = 1 if t_need - t_now>=0.5 else 0
    neuron_dt_c = 1 if t_need - t_now<=-0.5 else 0

    neuron_up = 1 if neuron_dt_h-neuron_h>=1 else 0
    neuron_down = 1 if neuron_dt_c-neuron_c>=1 else 0
    neuron_stop = 1 if neuron_h+neuron_c-neuron_up-neuron_down>=1 else 0

    print('{},{},{},{}'.format(neuron_h,neuron_c,neuron_dt_h,neuron_dt_c))
    return neuron_up, neuron_down, neuron_stop

# for i in range(5):
#     s = [float(i) for i in input().split(' ')]
#     print(funControl(s[0],s[1],s[2]))

answer = 'jsdnfk#12.3#156#13#14#18#\r\n'
a = answer.split('#')[1:6]
print(a)