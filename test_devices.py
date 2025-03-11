import pyaudio
p = pyaudio.PyAudio()
devices_num  = p.get_device_count()

input_devices_list = []
output_devices_list = []

for i in range(devices_num):
    device  =  p.get_device_info_by_index(i)
    if(device['maxInputChannels'] > 0):
        input_devices_list.append(device)
    elif(device['maxOutputChannels'] > 0):
        output_devices_list.append(device)
print("input devices list:")
for device in input_devices_list:
    print(device)

print("output devices list:")
for device in output_devices_list:
    print(device)