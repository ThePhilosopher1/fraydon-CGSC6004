#################### ham cheese production model ###################


import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class coffeeshop(ccm.Model):        # items in the environment look and act like chunks - but note the syntactic differences
    coffee=ccm.Model(isa='coffee',location='on_table')
    milk=ccm.Model(isa='milk',location='on_table')
    cream=ccm.Model(isa='cream',location='on_table')
    sugar=ccm.Model(isa='sugar',location='on_table')

class MotorModule(ccm.Model):     # create a motor module do the actions 
    def coffee(self):           # note that technically the motor module is outside the agent
        yield 2                   # but it is controlled from within the agent, i.e., it bridges the cognitive and the environment
        print "do the coffee"
        self.parent.parent.coffee.location='on_plate'    # self=MotorModule, parent=MyAgent, parent of parent=Subway
    def milk(self):     
        yield 2                   # yield refers to how long the action takes, but cognition can continue while waiting for an action to complete
        print "do the milk"
        self.parent.parent.milk.location='on_plate'   # in this case the motor actions make changes to the environment objects
    def cream(self):     
        yield 2
        print "do the cream"
        self.parent.parent.cream.location='on_plate'
    def sugar(self):     
        yield 2
        print "do the sugar"
        self.parent.parent.sugar.location='on_plate'
        
class MyAgent(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('coffee')

    def coffee(focus='coffee beans'):
        print "I have a cup of coffee"     
        focus.set('coffee milk')
        motor.do_coffee()                  # direct the motor module to do an action

    def milk(focus='coffee milk', coffee='location:on_plate'):   # production fires off the environment directly
        print "I have the milk"                                         # this is legitimate if it is assumed that the agent is... 
        focus.set('coffee cream')                                     # continuously and successfully monitoring the envionment
        motor.do_milk()                                             # and time for monitoring is incorporated into the action time

    def cream(focus='coffee cream', milk='location:on_plate'):        # slot name required for objects
        print "I have the cream"
        focus.set('coffee sugar')
        motor.do_cream()

    def sugar(focus='coffee sugar', cream='location:on_plate'):
        print "I have the sugar"
        focus.set('stop')
        motor.do_sugar()

    def stop_production(focus='stop', sugar='location:on_plate'):  # wait for the action to complete before stopping
        print "I have made cup of coffee"
        self.stop()


tim=MyAgent()
env=coffeeshop()
env.agent=tim 
ccm.log_everything(env)

env.run()
ccm.finished()
