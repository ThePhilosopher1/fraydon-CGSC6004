#################### ham cheese forgetting DM model ###################

# this model turns on the subsymbolic processing for DM, which causes forgetting


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

    DMbuffer=Buffer()                   
    DM=Memory(DMbuffer,latency=1.0,threshold=0)   # latency controls the relationship between activation and recall
                                                     # activation must be above threshold - can be set to none
            
    dm_n=DMNoise(DM,noise=0.0,baseNoise=0.0)         # turn on for DM subsymbolic processing
    dm_bl=DMBaseLevel(DM,decay=0.5,limit=None)       # turn on for DM subsymbolic processing


    def init():
        DM.add('customer:customer1 order:42')
        focus.set('rehearse')
                                        
    def request_chunk(focus='rehearse'):  
        print "recalling the order"
        DM.request('customer:customer1 order:?42')            
        focus.set('recall') 

    def recall_chunk(focus='recall', DMbuffer='customer:customer1 order:?order'):  
        print "Customer 1 wants......."         
        print order                     # note - outside the quotes you do not need the ?       
        DM.add('customer:customer1 ?order')      # but inside you do   
        DMbuffer.clear()                    # each time you put something in memory (DM.add) it increases activation
        focus.set('rehearse')

    def forgot(focus='recall', DMbuffer=None, DM='error:True'):
                                           # DMbuffer=none means the buffer is empty
                                           # DM='error:True' means the search was unsucessful
        print "I recall they wanted......."
        print "I forgot"
        focus.set('stop')



tim=MyAgent()                              # name the agent
burgershop=MyEnvironment()                     # name the environment
burgershop.agent=tim                           # put the agent in the environment
ccm.log_everything(burgershop)                 # print out what happens in the environment
log=ccm.log(html=True)
burgershop.run(2)                               # run the environment FOR 2 SECONDS
ccm.finished()                             # stop the environment
