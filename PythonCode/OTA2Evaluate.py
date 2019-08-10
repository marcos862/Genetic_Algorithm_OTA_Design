import functionsToEvaluate as fn
import subprocess
import os

path2baseCircuit = r'D:\Marcos\Skydrive\Dropbox\Academicos (Escuela)\02_ITESO\05_Semestre\Analisis y Diseno de Algoritmos\ProyectoFinal\Circuit\OTA_Basic.net'
path2LTSpice = r'C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe'
path2TempCircuits = r'C:\temp\temp_Circuits'

BW_array = []
Gain_array = []
Fitness_array = []

class OTA_Basic():
    def __init__(self, BW, Gain):
        self.BW = BW
        self.Gain = Gain

    def getRangeX1(self):
        return [1.2, 300.0]

    def getRangeX2(self):
        return [1.2, 300.0]

    def evaluate(self, x1, x2):
        path2Circuit = self._overwriteParams(x1, x2)
        self._runLTSpice(path2Circuit)
        return self._getBWandGain(path2Circuit)

    def getFitness(self, value):
        BW_t = value[0]
        Gain_t = value[1]
        if BW_t > self.BW:
            BW_f = 1
        else:
            BW_f = BW_t / self.BW
        if Gain_t > self.Gain:
            Gain_f = 1
        else:
            Gain_f = Gain_t / self.Gain
        fitness = (BW_f + Gain_f) / 2
        Fitness_array.append(fitness)
        return fitness

    def _runLTSpice(self, path2Circuit):
        p = subprocess.Popen([path2LTSpice, '-b', path2Circuit, '-Run'])
        while p.poll() != 0:
            pass

    def _overwriteParams(self, NMOS_w, PMOS_w):
        Source_netlist = open(path2baseCircuit, 'r')
        circuit_filename = os.path.basename(path2baseCircuit)
        if not os.path.lexists(path2TempCircuits):
            os.mkdir(path2TempCircuits)
        netlist_filename_mod = circuit_filename.replace('.net', '_0.net')
        count = 0
        path2Mod_Netlist = os.path.join(path2TempCircuits, netlist_filename_mod)
        while os.path.lexists(path2Mod_Netlist):
            count = count + 1
            path2Mod_Netlist = path2Mod_Netlist.replace('_{}.net'.format(count - 1), '_{}.net'.format(count))
        Mod_netlist = open(path2Mod_Netlist, 'w')
        for newline in Source_netlist:
            if newline.startswith('M1') or newline.startswith('M2') or newline.startswith('M5') or newline.startswith('M6'):
                newline_splited = newline.split(' ')
                newline = newline_splited[0]
                for i in range(1, 7):
                    newline = '{} {}'.format(newline, newline_splited[i])
                if newline.startswith('M1') or newline.startswith('M2'):
                    line_mod = 'w={}u\n'.format(NMOS_w)
                else:
                    line_mod = 'w={}u\n'.format(PMOS_w)
                newline = '{} {}'.format(newline, line_mod)
            Mod_netlist.write(newline)
        Source_netlist.close()
        Mod_netlist.close()
        return path2Mod_Netlist

    def _getBWandGain(self, path2Circuit, rmv_raw_files = True):
        logfilename = path2Circuit.replace('.net', '.log')
        logfile = open(logfilename, 'r')
        gain = 0.0
        bw = 0.0
        for line in logfile:
            if line.startswith('gain'):
                gain_line = line.split('=')
                gain_line = gain_line[1].split(',')
                gain_line = gain_line[0].replace('(', '')
                gain_line = gain_line.replace('dB', '')
                gain = float(gain_line)
            if line.startswith('bw'):
                bw_line = line.split('AT')
                bw_line = bw_line[1].replace(' ', '')
                bw_line = bw_line.replace('r', '')
                bw = float(bw_line)
        if rmv_raw_files:
            raw_files = logfilename.replace('.log', '.raw')
            os.remove(raw_files)
            raw_files = logfilename.replace('.log', '.op.raw')
            os.remove(raw_files)
        BW_array.append(bw)
        Gain_array.append(gain)
        return [bw, gain]

def main():
    BW = 2e6
    Gain = 80 # This is in dB
    global path2baseCircuit
    #path2baseCircuit = r'C:\Users\marco\Documents\ProyectoFinal\Circuit\OTA_Basic.net'
    path2baseCircuit = r'/home/Marcos862/Dropbox/academicos (escuela)/02_ITESO/05_Semestre/Analisis y Diseno de Algoritmos/ProyectoFinal/Circuit/OTA_Basic.net'
    

    t = OTA_Basic(BW, Gain)

    path2Circuit = t._overwriteParams(22.3814, 1.2638)
    t._runLTSpice(path2Circuit)
    bw, gain = t._getBWandGain(path2Circuit)

    print ("BW = {}, Gain = {}".format(bw, gain))

if __name__ == '__main__':
    main()
