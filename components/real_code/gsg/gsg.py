import time
import math
import components.real_code.gsg.MPU6050 as MPU6050

def run_gsg_loop(delay, threshold, callback, stop_event):
    mpu = MPU6050.MPU6050()
    mpu.dmp_initialize()

    baseline = None

    while not stop_event.is_set():
        accel = mpu.get_acceleration()

        x = accel[0] / 16384.0
        y = accel[1] / 16384.0
        z = accel[2] / 16384.0

        magnitude = math.sqrt(x*x + y*y + z*z)

        if baseline is None:
            baseline = magnitude

        if abs(magnitude - baseline) > threshold:
            callback(True)

        time.sleep(delay)
