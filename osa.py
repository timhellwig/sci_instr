""" Scientific - Instrumentation module based on pyvisa

"""

__author__ = 'Tim Hellwig'



import sci_instr.generic
import os



class AQ6370C(sci_instr.generic.Instrument):
    """Allows easy communication with Yokogawa OSA AQ6370C"""  
    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(AQ6370C, self).__init__(visa_rm,address,conffile=os.path.join('Osa','AQ6370C.yaml'))
        
        self._visa.write(':init:smode 1;*CLS";:init')
        
    def start_sweep():
        """Sends the trigger to start a sweep"""
        self._visa.write('*CLS";:init')
        
    def is_ready(self):
        """ Query the instrument whether it has succesfully completed
        all operations"""
        out = self._visa.query(':stat:oper:even?')
        
        return bool(out[0])
    
        
