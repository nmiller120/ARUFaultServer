# Module defines program constants

faultPin = (35, 33, 31, 29, 40) # 5 bits, 32 possible states, 35 (0) msb, 40 (4) lsb
latchPin = 37
errorLED = 36
statusLED = 38
faultString = ["Supply Fan Overlad Tripped", "Dirty Filter", "Gas Leak Detected",
            "Smoke Detected", "Front Fan Start Failure",
            "ASH Safeties", "Outside Damper Limit Switch Not Open",
            "Outside Damper Limit Switch Not Closed", "Control Power Loss",
            "Start Enable PB Must Be Pressed", "Supply Disconnect Open",
            "Rear Fan Start Failure", "Supply Fan Start Failure",
            "Invalid Burner Differential Pressure", "High Temperature Thermostat",
            "Low Temperature Thermostat", "High Discharge Temperature",
            "Low Discharge Temperature", "Invalid Space Temperature",
            "PLC Low Battery", "PLC Faulted", "High Gas Pressure",
            "Low Gas Pressure", "Flame Relay Alarm", "Burner Failure",
            "Fan Vibration", "Flame Failure"]
