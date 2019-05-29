""" Scientific - Instrumentation module based on pyvisa

implements different Oscilloscopes
"""

__author__ = 'Tim Hellwig'



import sci_instr.generic
import os
import numpy as np


class RS_RTO1044(sci_instr.generic.Instrument):
    """Allows easy communication with R&S Oscilloscope RTO1044"""  
    
    def __init__(self,visa_rm,address):
        """Call generic init to connect and prepare instrument"""
        super(RS_RTO1044, self).__init__(visa_rm,address,conffile=os.path.join('Oscilloscopes','RS_RTO1044.yaml'))
        
        self._visa.write('FORM REAL,32;')
     
        
    def is_ready(self):
        """ Query the instrument whether it has succesfully completed
        all operations"""
        out = self._visa.query(':stat:oper:even?')
        
        return bool(out[0])
    
    def reset_stat(self,meas_number):
        """ Resets the statistics of active measurement meas_number"""
        self._visa.write("MEASurement{}:STATistics:RESet".format(int(meas_number)))




class Tktx_DP7254(sci_instr.generic.Instrument):
    """Allows easy communication with Tektronix Oscilloscope DPO7254"""  
    
    def __init__(self,visa_rm,address):
        """Call generic init to connect and prepare instrument"""
        super(Tktx_DP7254, self).__init__(visa_rm,address,conffile=os.path.join('Oscilloscopes','Tktx_DP7254.yaml'))
        self._visa.write('DATA:ENC RPB')
        self._visa.write('WFMOutpre:BYT_NR 1')
        self._visa.write('DATA:START 1')
        length = self._visa.query('HORIZONTAL:ACQLENGTH?')
        self._visa.write('DATA:STOP ' + length)
        
        self._visa.values_format.use_binary('B', False, np.array)
        
    def is_ready(self):
        """ Query the instrument whether it has succesfully completed
        all operations"""
        out = self._visa.query('BUSY?')
        return bool(out[0])
    
    def reset_stat(self):
        """ Resets the statistics of existing measurements"""
        self._visa.write("MEASUREMENT:STATISTICS:COUNT RESET")
        
    def getTrace(self, trace='next'): #todo: does not work!!!
        # get scaling parameters
        ymult = self.yscale
        yzero = self.yoffset
        yoff = self.doffset
        xincr = self.xincrement
        # query values
        if trace=='current':
            val = self.curve
        elif trace=='next':
            val = self.nextcurve
        else:
            print('Trace is not specified as current or next!')
        # calculate the correct axes
        volts = (val - yoff) * ymult  + yzero
        time = np.arange(0, xincr * len(volts), xincr)
        # return time and volt array
        return time, volts