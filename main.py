from watch import Watch
import time

print("Welcome to nicolaWCH")

watch = Watch(mpu_address=0x68)

datetime = (2025, 10, 10, 4, 19, 3, 0, 0)
watch.set_datetime(datetime)

while True:
    time.sleep(0.05)
    watch.update()
