from classes.CustomButton import CustomButton
class PWMStepperMotorTest():

    #add a tag to the motor
    def __init__(self, step: int, drive: int, direction_forward=True):
        """
        Default Class initializer with that accepts the Output device pin.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        self.step = step
        self.drive = drive
        self.direction_forward = direction_forward
    
    def setMotor(self, step: int, drive: int, direction_forward=True):
        """
        Setup and pin out output device.

        Parameters:
        -----------
        step: int
            - stepper pin value.
        drive: int
            - drive pin value.
        direction_forward: bool
            - direction of the motor.

        Return:
        -------
        None
        """
        self.direction_forward = direction_forward

    
    def rotate_motor(self, direction):
        """
        Rotate the specified motor one step.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        """"""
        print(f"rotate motor: {direction}")


pins = [{'down': 18, 'right': 21, 'up': 26, 'left': 20, 'trigger': 13, 'fire': 19}]
movements = {
            'pins': {'down': 18, 'right': 21, 'up': 26, 'left': 20}, 
            'motors': [{
                'step': 1, 
                'drive': 2, 
                'direction': True, 
                'movement': 'up'}, {
                'step': 3, 
                'drive': 4, 
                'direction': True, 
                'movement': 'up'}]}

down_movement: CustomButton = CustomButton(18, tag='down', pull_up=True)
up_movement: CustomButton = CustomButton(26, tag='up', pull_up=True)
right_movement: CustomButton = CustomButton(21, tag='right', pull_up=True)
left_movement: CustomButton = CustomButton(20, tag='left', pull_up=True)
trigger_movement: CustomButton = CustomButton(13, tag='trigger', pull_up=True)
fire_movement: CustomButton = CustomButton(19, tag='fire', pull_up=True)

directional_movements = []
button_registry = {}
motor_registry = {}

# Function to register a button
def register_button(tag, button):
    if tag in button_registry:
        print(f"Warning: Button with tag '{tag}' already exists.")
    else:
        button_registry[tag] = button

# Function to get a button by its tag
def get_button_by_tag(tag):
    return button_registry.get(tag)

# Function to register a button
def register_motor(tag, motor):
    if tag in motor_registry:
        print(f"Warning: Motor with tag '{tag}' already exists.")
    else:
        motor_registry[tag] = motor

# Function to get a button by its tag
def get_motor_by_tag(tag):
    return motor_registry.get(tag)

def valid_index(lst, index):
    try:
        lst[index] 
        return True 
    except IndexError:
        return False


def setUpMovements(): 
    for devices in pins:
        for key, value in devices.items():
            addMovement(key, value)
                
def addMovement(movement: str, 
                pin: int):
    print(f"movement: {movement}")
    if movement == 'right':
       right_movement = CustomButton(pin, tag=movement, pull_up=True)
    elif movement == 'down':
        down_movement =  CustomButton(pin, tag=movement, pull_up=True)
    elif movement == 'up':
        up_movement =  CustomButton(pin, tag=movement, pull_up=True)
    elif movement == 'left':
        left_movement =  CustomButton(pin, tag=movement, pull_up=True)
    elif movement == 'trigger':
        trigger_movement =  CustomButton(pin, tag=movement, pull_up=True)         
    elif movement == 'fire':
        fire_movement = CustomButton(pin, tag=movement, pull_up=True)

def monitorMovements():
    print(f"self.movements : {movements}")
    while True:
       if down_movement.is_active:
            print(f"check down movement: {get_motor_by_tag(down_movement.tag)}")
            if get_motor_by_tag(down_movement.tag) != None:
                down_motor: PWMStepperMotorTest = get_motor_by_tag(down_movement.tag)
                down_motor.rotate_motor(down_movement.tag)
       elif right_movement.is_active:
            if get_motor_by_tag(right_movement.tag) != None:
                right_motor: PWMStepperMotorTest = get_motor_by_tag(right_movement.tag)
                right_motor.rotate_motor(right_movement.tag)
       elif up_movement.is_active:
             if get_motor_by_tag(up_movement.tag) != None:
                _motors = get_motor_by_tag(up_movement.tag)
                if len(_motors) > 1:
                    #have to manually check the motors added minimum of 2 motors  
                    if valid_index(_motors, 0):
                        motor1: PWMStepperMotorTest = _motors[0]
                        motor1.rotate_motor(up_movement.tag)
                    if valid_index(_motors, 1):
                        motor2: PWMStepperMotorTest = _motors[1]
                        motor2.rotate_motor(up_movement.tag)    
                else:
                    up_motor: PWMStepperMotorTest = _motors[0]
                    up_motor.rotate_motor(up_movement.tag)    
       elif left_movement.is_active:
           if get_motor_by_tag(left_movement.tag) != None:
                left_motor: PWMStepperMotorTest = get_motor_by_tag(left_movement.tag)
                left_motor.rotate_motor(left_movement.tag)  
       elif trigger_movement.is_active:
            print(f"pingiw pingiw bang bang ") 
       elif fire_movement.is_active:
            print(f"fire in the hole")                        
            
def configureMovement():
    if "motors" in movements:
        motors = movements.get('motors')
        for item in motors:
            print(f"motors : {item.get('step')}")
            #this code needs to be tested
            if item.get('movement') in motor_registry:
                _motors = motor_registry.get(item.get('movement'))
                print(f"motors movement: {_motors }")
                _motors.append(PWMStepperMotorTest(item.get('step'), 
                                          item.get('drive'),
                                          item.get('direction')))
            else:    
                register_motor(item.get('movement'), [PWMStepperMotorTest(item.get('step'), 
                                                                          item.get('drive'),
                                                                          item.get('direction'))])

configureMovement()
monitorMovements()            