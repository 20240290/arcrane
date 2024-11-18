from classes.CustomButton import CustomButton
from classes.PWMStepperMotor import PWMStepperMotor
import constants as const
class PWMStepperMotorTest():

    def __init__(self, step: int, drive: int, direction_forward=True, reversable=False, reverse_movement = '', movement = ''):
        """
        Default Class initializer with that accepts the Output device pin.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        self.motor_step = step
        self.motor_dir = drive
        self.step = step
        self.drive = drive
        self.direction_forward = direction_forward
        self.movement = movement
        self.reversable = reversable
        self.reverse_movement = reverse_movement
    
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

    
    def rotate_motor2(self, direction):
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
            'pins': {'down': 18, 'right': 21, 'up': 26, 'left': 20, 'trigger': 13, 'fire': 19}, 
            'motors': [{
                'step': const.M1_STEP_PIN, 
                'drive': const.M1_DIR_PIN, 
                'direction': True,
                'reversable': True, 
                'reverse_movement': 'down',
                'movement': 'up'},{
                'step': const.M2_STEP_PIN, 
                'drive': const.M2_DIR_PIN, 
                'direction': True, 
                'reversable': True, 
                'reverse_movement': 'down',
                'movement': 'up'}, {
                'step': const.M3_STEP_PIN, 
                'drive': const.M3_DIR_PIN, 
                'direction': True, 
                'reversable': False, 
                'reverse_movement': '',
                'movement': 'left'}, {
                'step': const.M4_STEP_PIN, 
                'drive': const.M4_DIR_PIN, 
                'direction': True, 
                'reversable': False, 
                'reverse_movement': 'down',
                'movement': 'right'}]}
                 

down_movement: CustomButton = CustomButton(18, tag='down', pull_up=True)
up_movement: CustomButton = CustomButton(26, tag='up', pull_up=True)
right_movement: CustomButton = CustomButton(21, tag='right', pull_up=True)
left_movement: CustomButton = CustomButton(20, tag='left', pull_up=True)
trigger_movement: CustomButton = CustomButton(13, tag='trigger', pull_up=True)
fire_movement: CustomButton = CustomButton(19, tag='fire', pull_up=True)

directional_movements = []
button_registry = {}
motor_registry = {}
lastMotorRotation = True

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
    #print(f"self.movements : {movements}")
    while True:

       if down_movement.is_active:
            print("down movement")
            #print(f"check down movement: {get_motor_by_tag(down_movement.tag)}")
            if get_motor_by_tag(down_movement.tag) != None:
                _motors = get_motor_by_tag(down_movement.tag)
                print("down more than 1")
                if len(_motors) > 1:
                    #have to manually check the motors added minimum of 2 motors  
                    if valid_index(_motors, 0):
                        motor1: PWMStepperMotorTest = _motors[0]
                        if (motor1.reversable &  (down_movement.tag == motor1.reverse_movement)):
                            motor1.rotate_motor2(not motor1.direction_forward)
                        else:
                            motor1.rotate_motor2(motor1.direction_forward)

                    if valid_index(_motors, 1):
                        motor2: PWMStepperMotorTest = _motors[1]
                        if (motor2.reversable &  (down_movement.tag == motor2.reverse_movement)):
                            motor2.rotate_motor2(not motor2.direction_forward)
                        else:
                            motor2.rotate_motor2(motor2.direction_forward)
                else:
                    down_motor: PWMStepperMotorTest = _motors[0]
                    if (down_motor.reversable &  (down_movement.tag == down_motor.reverse_movement)):
                        down_motor.rotate_motor2(not down_motor.direction_forward) 
                    else:
                        down_motor.rotate_motor2(down_motor.direction_forward)
       elif right_movement.is_active:
            print("right movement")
            if get_motor_by_tag(right_movement.tag) != None:
                _motors = get_motor_by_tag(right_movement.tag)
                right_motor: PWMStepperMotorTest = _motors[0]
                right_motor.rotate_motor2(right_motor.direction_forward)
       elif up_movement.is_active:
            print("down movement")
            if get_motor_by_tag(up_movement.tag) != None:
                _motors = get_motor_by_tag(up_movement.tag)
                if len(_motors) > 1:
                    print("up more than 1")
                    #have to manually check the motors added minimum of 2 motors  
                    if valid_index(_motors, 0):
                        motor1: PWMStepperMotorTest = _motors[0]
                        if (motor1.reversable &  (up_movement.tag == motor1.reverse_movement)):
                            motor1.rotate_motor2(not motor1.direction_forward)    
                        else:
                            motor1.rotate_motor2(motor1.direction_forward) 
                    if valid_index(_motors, 1):
                        motor2: PWMStepperMotorTest = _motors[1]
                        if (motor2.reversable &  (up_movement.tag == motor2.reverse_movement)):
                            motor2.rotate_motor2(not motor2.direction_forward)    
                        else:
                            motor2.rotate_motor2(motor2.direction_forward) 
                else:
                    up_motor: PWMStepperMotorTest = _motors[0]
                    #print(f"up else: {up_motor.direction_forward} tag: {up_movement.tag}")
                    if (up_motor.reversable &  (up_movement.tag == up_motor.reverse_movement)):
                        up_motor.rotate_motor2(not up_motor.direction_forward)    
                    else:
                        up_motor.rotate_motor2(up_motor.direction_forward)    
                        
       elif left_movement.is_active:
           print("left movement")
           if get_motor_by_tag(left_movement.tag) != None:
                _motors = get_motor_by_tag(left_movement.tag)
                left_motor: PWMStepperMotorTest = _motors[0]
                left_motor.rotate_motor2(left_motor.direction_forward)  
       elif trigger_movement.is_active:
            pass
            #print(f"pingiw pingiw bang bang ") 
       elif fire_movement.is_active:
            pass
            #print(f"fire in the hole")                        
            
def configureMovement():
    if "motors" in movements:
        motors = movements.get('motors')
        for item in motors:
            print(f"motors : {item}")
            #this code needs to be tested
            movement = item.get('movement')
            print(f"configure movement is: {movement}")
            if movement in motor_registry:
                _motors: list = motor_registry.get(movement)
                print(f"number of motors with the same movement: { len(_motors) }")
                if item.get('reversable'): 
                    reversible_motor = PWMStepperMotorTest(item.get('step'), item.get('drive'),item.get('direction'), item.get('reversable'), item.get('reverse_movement'), movement)
                    _motors.append(reversible_motor)
                    motor_registry[movement] = _motors

                    if item.get('reverse_movement') in motor_registry:
                        _reverseMotors: list = motor_registry.get(item.get('reverse_movement'))
                        _reverseMotors.append(reversible_motor)
                        motor_registry[movement] = _reverseMotors
                    print(f"number of motors with the same movement: { len(motor_registry.get(movement)) }")             
                else:
                   #print(f"motor is not reversable: {item.get('movement')} with item : {item}")
                   _motors.append(PWMStepperMotorTest(item.get('step'), 
                                          item.get('drive'),
                                          item.get('direction'), 
                                          item.get('reversable'), 
                                          item.get('reverse_movement'), 
                                          item.get('movement')))
                   register_motor(item.get('movement'), _motors)                                             
            else:
                print(f"does not exist") 
                if item.get('reversable'): 
                    #print(f"motor is reversable: {item.get('movement')} with item : {item}")
                    reversible_motor = PWMStepperMotorTest(item.get('step'), item.get('drive'),item.get('direction'), item.get('reversable'), item.get('reverse_movement'), movement)

                    register_motor(movement, [reversible_motor])
                    register_motor(item.get('reverse_movement'), [reversible_motor])
                                                                          
                else:
                   #print(f"motor is not reversable: {item.get('movement')} with item : {item}")     

                   register_motor(movement, [PWMStepperMotorTest(item.get('step'), 
                                                                          item.get('drive'),
                                                                          item.get('direction'), 
                                                                          item.get('reversable'), 
                                                                          item.get('reverse_movement'), 
                                                                          movement)])

configureMovement()
monitorMovements()            