from pyrobot.brain import Brain
import Avoid as av
import math

class BrainTestNavigator(Brain):
 
  NO_FORWARD = 0
  SLOW_FORWARD = 0.1
  MED_FORWARD = 0.5
  FULL_FORWARD = 1.0

  GEAR1 = 0.1
  GEAR2 = 0.45
  GEAR3 = 0.5
  GEAR4 = 0.9
  LOW_RIGHT = 0.2
  MED_RIGHT = 0.4
  HARD_RIGHT = 0.7
  LOW_LEFT = -0.2
  MED_LEFT = -0.4
  HARD_LEFT = -0.7

  NO_TURN = 0
  # MED_LEFT = 0.5
  # HARD_LEFT = 1.0
  # MED_RIGHT = -0.5
  # HARD_RIGHT = -1.0

  NO_ERROR = 0.2
  NO_ERROR2 = -0.2

  def setup(self):
    pass

  # # Give the front two sensors, decide the next move  
  # def determineMove(self, front, left, right):  
  #   if front < 0.5:   
  #     #print "hay obstaculo en frente, giro 90grad y sigo"  
  #     return(0, 1)   
  #   elif right == 0: 
  #     #print "object detected on right, slow turn" 
  #     return(0, 1)  
  #   else:  
  #     #print "clear"  
  #     return(0.6, 0.0) 

  def step(self):
    hasLine,lineDistance,searchRange = eval(self.robot.simulation[0].eval("self.getLineProperties()"))
    print "I got from the simulation",hasLine,lineDistance,searchRange
    front = min([s.distance() for s in self.robot.range["front"]])
    left = min([s.distance() for s in self.robot.range["left-front"]])
    right = min([s.distance() for s in self.robot.range["right-front"]])
    
    # if (hasLine and front>0.4 or hasLine and front==0):
    #   if (lineDistance>2):
    #     self.move(0,lineDistance/2)
    #   elif (lineDistance > 0.6):
    #     self.move(self.GEAR1,self.HARD_RIGHT)
    #   elif (lineDistance > 0.3):
    #     self.move(self.GEAR1,self.MED_RIGHT)
    #   elif (lineDistance > 0.2):
    #     self.move(self.GEAR2,self.LOW_RIGHT)
    #   elif (lineDistance < -2):
    #     self.move(0,lineDistance/2)
    #   elif (lineDistance < -0.6):
    #     self.move(self.GEAR2,self.HARD_LEFT)
    #   elif (lineDistance < -0.3):
    #     self.move(self.GEAR2,self.MED_LEFT)
    #   elif (lineDistance < -0.2):
    #     self.move(self.GEAR1,self.LOW_LEFT)
    #   else:
    #     self.move(self.GEAR4,self.NO_TURN)
    
    if(hasLine and front>0.5 or hasLine and front==0):
      tv = lineDistance/2
      i = abs(tv*1.5)
      i = 1-i
      fv = max(0,i)
      if fv == 0:
        fv = 0.05
      self.move(fv,tv)
    else:
      #self.move(0,1)
      # if we can't find the line we just stop, this isn't very smart
      print "front: " + str(front)
      print "right: " + str(right)
      if front < 0.7:
        self.robot.move(0.2,1.5)
      elif right<0.5:   
        #print "hay obstaculo en frente, giro 90grad y sigo"  
        self.robot.move(0.1, 0.2)
      elif right > 9:
        self.robot.move(0.2, -1.5)
      else:  
        print "clear" 
        self.robot.move(0.1, 0)
      #self.move(0.2,0.2) 

    

def INIT(engine):
  assert (engine.robot.requires("range-sensor") and
	  engine.robot.requires("continuous-movement"))

  # If we are allowed (for example you can't in a simulation), enable
  # the motors.
  try:
    engine.robot.position[0]._dev.enable(1)
  except AttributeError:
    pass

  return BrainTestNavigator('BrainTestNavigator', engine)
