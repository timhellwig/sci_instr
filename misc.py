""" Scientific - Instrumentation module based on pyvisa

implements misc sort of instruments not fitting other categories

"""

__author__ = 'Tim Hellwig'



import sci_instr.generic
import os
import re



class Katana(sci_instr.generic.Instrument):
    """Allows easy communication with OneFive Katana
    
    uses non standard set command (=) and wants only integer numbers,
    as well as answers with "done\r\n" to each setting change!
    
    """  
    
    _getString = '?'
    _setString = '='
    _expctResponse = 'done\r\n'
    _formatString = '{:d}'
    
    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(Katana, self).__init__(visa_rm,address,conffile=os.path.join('Misc','Katana.yaml'))
        
        self._visa.baud_rate = 19200
        self._visa.encoding='windows-1252'


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
     

            
            
        
