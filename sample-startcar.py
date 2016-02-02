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
        focus.set('goal:startcar object:car')

    def seeing_car(focus='goal:startcar object:car'):     # if focus buffer has this chunk then....
        print "I see my car"                            # print
        focus.set('goal:startcar object:get_in_car')                   # change chunk in focus buffer

    def get_in_car(focus='goal:startcar object:get_in_car'):          # the rest of the productions are the same
        print "I am inside my car"                # but carry out different actions
        focus.set('goal:startcar object:put_key_in_ignition')

    def put_key_in_ignition(focus='goal:startcar object:put_key_in_ignition'):
        print "I have put the key in the ignition"
        focus.set('goal:startcar object:turn_key')

    def turn_key(focus='goal:startcar object:turn_key'):
        print "I have turned the key"
        print "I have started the car"
        focus.set('goal:stop')   

    def stop_production(focus='goal:stop'):
        self.stop()                                           # stop the agent

tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
