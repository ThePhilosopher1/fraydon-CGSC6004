import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

#####
# Python ACT-R requires an environment
# but in this case we will not be using anything in the environment
# so we 'pass' on putting things in there

class MyEnvironment(ccm.Model):
    pass

#####
# create an act-r agent

class MyAgent(ACTR):
    
    focus=Buffer()

    def init():
        focus.set('goal:pizza object:dough')

    def dough (focus='goal:pizza object:dough'):     # if focus buffer has this chunk then....
        print "I have made a round piece of dough"                            # print
        focus.set('goal:pizza object:cheese')                   # change chunk in focus buffer

    def cheese(focus='goal:pizza object:cheese'):          # the rest of the productions are the same
        print "I have put cheese on the dough"                # but carry out different actions
        focus.set('goal:pizza object:ham')

    def chicken(focus='goal:pizza object:ham'):
        print "I have put chicken on the cheese"
        focus.set('goal:pizza object:sauce')

    def sauce(focus='goal:pizza object:cheese'):
        print "I have put sauce on the chicken"
        print "I have made a chicken and cheese pizza"
        focus.set('goal:stop')   

    def stop_production(focus='goal:stop'):
        self.stop()                                           # stop the agent

tim=MyAgent()                              # name the agent
pizzashop=MyEnvironment()                     # name the environment
pizzashop.agent=tim                           # put the agent in the environment
ccm.log_everything(pizzashop)                 # print out what happens in the environment

pizzashop.run()                               # run the environment
ccm.finished()                             # stop the environment

