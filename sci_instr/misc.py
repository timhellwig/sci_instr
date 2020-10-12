""" Scientific - Instrumentation module based on pyvisa

implements misc sort of instruments not fitting other categories

"""

__author__ = 'Tim Hellwig'



import sci_instr.generic
import os
import re
import visa
import numpy as np



        


class Katana(sci_instr.generic.Instrument):
    """Allows easy communication with OneFive Katana
    
    uses non standard set command (=) and wants only integer numbers,
    as well as answers with "done\r\n" to each setting change!
    
    """  
    
    _getString = ''
    _setString = '='
    _expctResponse = 'OK'
    _formatString = '{:d}'
    
    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(Katana, self).__init__(visa_rm,address,conffile=os.path.join('Misc','Katana.yaml'))
        
        self._visa.baud_rate = 19200
        self._visa.encoding='windows-1252'
        
        # flush the read buffer as the katana seems to be stuck in a
        # debug output sometimes
        self._visa.flush(visa.constants.VI_READ_BUF_DISCARD)


    def _process_read_values(self,msg):
        """Find the numbers in Katanas long msg and parse on/off as 1/0 for
        laser status"""
        
        #print(msg)
        out = re.findall(r"[-+]?\d*\.\d+|\d+",msg)
        if out:
            return float(out[0])
        else:
            if not msg.find(' on\r\n')==-1:
                return 1
            elif not msg.find(' off\r\n')==-1:
                return 0
                
    def debug(self):
        out = ''
        self._visa.write('debug?')
        for i in range(0,27):
            out = out + self._visa.read()
                                   #join them to one byte String
        print(out)  #decode the byte String into something printable
        
        


class Manson_HSC3202():
    """Allows easy communication with OneFive Katana
    
    uses non standard set command (=) and wants only integer numbers,
    as well as answers with "done\r\n" to each setting change!
    
    """  
    
    _getString = '?'
    _setString = '='
    _expctResponse = 'OK'
    _formatString = '{:d}'
    
    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        self._visa = visa_rm.open_resource(address)
        
        self._visa.baud_rate = 9600
        self._visa.read_termination='\r'
        self._visa.write_termination = '\r'
        
        # flush the read buffer as the katana seems to be stuck in a
        # debug output sometimes
        self._visa.flush(visa.constants.VI_READ_BUF_DISCARD)

    
    @property
    def current(self):
        temp = self._read_value('GETS')
        curr = float(temp[3:6])/10
        return curr

    @current.setter
    def current(self, value):
        if value>10.0 or value<0.0:
            raise AttributeError('Value out of limits')
        else:
            value = "{:03d}".format(int(value*10))
            self._write_value('CURR',value)
            
    @property
    def volt(self):
        temp = self._read_value('GETS')
        volt = float(temp[1:3])/10
        return volt
    @volt.setter
    def volt(self, value):
        if value>36.0 or value<0.0:
            raise AttributeError('Value out of limits')
        else:
            value = "{:03d}".format(int(value*10))
            self._write_value('VOLT',value)
            
    @property
    def max_volt(self):
        max_volt = self._read_value('GOVP')
        max_volt = float(max_volt)/10
        return max_volt
    @max_volt.setter
    def max_volt(self, value):
        if value>36.0 or value<0.0:
            raise AttributeError('Value out of limits')
        else:
            value = "{:03d}".format(int(value*10))
            self._write_value('SOVP',value)
            
    @property
    def max_current(self):
        max_curr = self._read_value('GOCP')
        max_curr = float(max_curr)/10
        return max_curr
    @max_current.setter
    def max_current(self, value):
        if value>10.0 or value<0.0:
            raise AttributeError('Value out of limits')
        else:
            value = "{:03d}".format(int(value*10))
            self._write_value('SOCP',value)
            
    def output_on(self):
        self._write_value('SOUT','0')
        
    def output_off(self):
        self._write_value('SOUT','1')
            
            
    
    def _read_value(self,command):
        out = self._visa.query(command)
        response = self._visa.read()
        if not response == self._expctResponse:
            msg = 'Response was: {}; expected: {}'.format(response,self._expctResponse)
            raise AttributeError(msg)
        return out
    
    def _write_value(self,command,value):
        out = self._visa.write(command+' '+value)
        response = self._visa.read() 
        if not response == self._expctResponse:
            msg = 'Response was: {}; expected: {}'.format(response,self._expctResponse)
            raise AttributeError(msg)
        return out
        
    def __del__(self):
        if self._visa is not None:
            self._visa.close()
        

class TL_PM100(sci_instr.generic.Instrument):
    """Allows easy communication with Thorlabs Powermeters PM100
    
    """  

    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(TL_PM100, self).__init__(visa_rm,address,conffile=os.path.join('Misc','TL_PM100.yaml'))
        
        
        

class TL_TSP01(sci_instr.generic.Instrument):
    """Allows easy communication with Thorlabs temperature monitor TL_TSP01
    
    """  

    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(TL_TSP01, self).__init__(visa_rm,address,conffile=os.path.join('Misc','TL_TSP01.yaml'))
                
        
        

class APE_PulseCheck_LR(sci_instr.generic.Instrument):
    """Allows easy communication with APE Pulse Check Long Range (not functional right now)
    
    uses non standard set command (=) and wants only integer numbers,
    as well as answers with "done\r\n" to each setting change!
    
    """  
    

    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(APE_PulseCheck_LR, self).__init__(visa_rm,address,conffile=os.path.join('Misc','APE_PulseCheck_LR.yaml'))
        self._visa.encoding='windows-1252'
        self._visa.baud_rate = 9600
        # self._visa.stop_bits = visa.constants.StopBits.one
        # self._visa.end_input = visa.constants.SerialTermination.termination_char
        # self._visa.flush(visa.constants.VI_READ_BUF_DISCARD)
        # self._visa.CR = '\n'
        # self._visa.LF = '\n'
        # self._visa.flow_control = visa.constants.VI_ASRL_FLOW_DTR_DSR
        
        #set paramters of device; GSR responds with 1 for scan range 2.1e-12 etc
        self._scan_ranges = (2.1e-12,4.3e-12,11e-12,30e-12,100e-12)
        self.scan_range = 2.1e-12;

        
        

     

            
            
        
