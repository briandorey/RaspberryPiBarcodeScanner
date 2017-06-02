from lib import Hardware
from lib import UI


def main():   
    # initialise hardware   
    hardware = Hardware.Hardware() 
    hardware.init_battery_monitor();
    hardware.init_scanner();

    # initialise and launch the UI
    app = UI.UI()



if __name__ == '__main__':
    main() 
