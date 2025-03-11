import pyaudio
p = pyaudio.PyAudio()
devices_num  = p.get_device_count()

devices_list = []

for i in range(devices_num):
    device  =  p.get_device_info_by_index(i)
    devices_list.append(device)
for device in devices_list:
    print(device)