try:
    from HX711.hx711 import HX711
except:
    from hx711 import HX711

class Massdetection():
    def __init__(self):
        self.reference_unit = 1

        self.hx = HX711(5, 6)
        self.hx.set_reading_format("MSB", "MSB")

        # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
        self.hx.set_reference_unit(922)

        self.hx.reset()
        self.hx.tare()
        print("Tare done! Add weight now...")

    def weight_input(self):
        val = self.hx.get_weight(5)
        return round(val)

if __name__ == "__main__":
    import time
    feeder = Massdetection()
    time.sleep(3)
    print(feeder.weight_input())
