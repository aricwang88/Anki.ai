from bluepy.btle import Scanner, DefaultDelegate
import re

# This Class represents the bluetooth information about the Anki OverDrive Car
class Car(object):
    macAddress = ''
    manufacturer = ''
    isCar = False
    isCharging = False

    def __init__(self, address):
        self.isCar = False
        self.macAddress = address

    def getMacAddress(self):
        return self.macAddress


    def setManufacturer(self, manufacturer):
        self.manufacturer = manufacturer

    def getCarId(self):
        if( len(self.manufacturer) >= 8):
            manArr = re.findall('..',self.manufacturer)
            return int(manArr[3],16)
        else:
            return ''

    def setIsCharging(self, isCharging):
        print( "setting is charging...")
        self.isCharging = isCharging

    def getIsCharging(self):
        return self.isCharging

    def setIsCar(self, isCar):
        self.isCar = isCar

    def getIsCar(self):
        return self.isCar

    def getCarName(self):
        if self.getCarId() == 1:
            return "Kourai"
        elif self.getCarId() == 2:
            return "Boson"
        elif self.getCarId() == 3:
            return "Rho"
        elif self.getCarId() == 4:
            return "Katal"
        elif self.getCarId() == 8:
            return "Ground Shock"
        elif self.getCarId() == 9:
            return "Skull"
        elif self.getCarId() == 10:
            return "Thermo"
        elif self.getCarId() == 11:
            return "Nuke"
        elif self.getCarId() == 12:
            return "Guardian"
        elif self.getCarId() == 14:
            return "Big Bang"
        elif self.getCarId() == 15:
            return "Free Wheel"
        elif self.getCarId() == 16:
            return "X52"
        elif self.getCarId() == 17:
            return "X52 Ice"
        else:
            return "UNKNOWN"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print( "Discovered device", dev.addr)
        elif isNewData:
            print( "Received new data from", dev.addr)

# This class scans bluetooth for turned-on Anki Overdrive Cars
class CarFactory(object):
    cars = []
    def __init__(self):
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(10.0)

        for dev in devices:
            #print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
            car = Car(dev.addr)
            for (adtype, desc, value) in dev.getScanData():
                #print ("  %s, %s = '%s'" % (adtype, desc, value))

                if adtype == 7 and value == 'f48d4d9cd80b81837e408661efbe15be':
                    car.setIsCar(True)

                if adtype == 255:
                    car.setManufacturer( value )

                if adtype == 9 and value.startswith('P'):
                    car.setIsCharging(True)
                    
            if car.getIsCar() == True:
                print( "Found a Anki Overdrive car:")
                print( " Mac address: %s " % car.getMacAddress())
                print( " Car ID:      %s " % car.getCarId())
                print( " Car Name:    %s " % car.getCarName())
                print( " Charging:    %s " % car.getIsCharging())
                self.cars.append(car)
    def getCars(self):
        return self.cars

# Example code: 
#cars = CarFactory()
#print( "Carfactory found %s cars " % len(cars.getCars()))
