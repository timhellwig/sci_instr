""" Scientific - Instrumentation module based on pyvisa

"""

__author__ = 'Tim Hellwig'



import sci_instr.generic
import os
import numpy as np



class AQ6370C(sci_instr.generic.Instrument):
    """Allows easy communication with Yokogawa OSA AQ6370C
    
    Note: Does only work when active trace is TRA
    """  
    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(AQ6370C, self).__init__(visa_rm,address,conffile=os.path.join('Osa','Yokogawa_AQ6370C.yaml'))
        
        self._visa.write(':init:smode 0;*CLS;:init')
        self._visa.write(':FORMat:DATA REAL,64')
        self._visa.values_format.use_binary('d', False, np.array)
        
    def start_sweep(self):
        """Sends the trigger to start a sweep"""
        self._visa.write('*CLS;:init')
        
    def is_ready(self):
        """ Query the instrument whether it has succesfully completed
        all operations"""
        out = self._visa.query('STAT:OPER:COND?')
        
        return bool(int(out[0]))
    
        
