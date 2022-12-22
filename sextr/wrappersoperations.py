import os

class readWriteCats:
    def __init__(self):
        self.config = {}

    def write_file(self, filename, mode='sex'):
        file = open(filename, 'w')
        file.write('#-- Config file generated by MAR pipeline --# \n')
        file.write('\n')
        file.write('\n')
        
        config = self.config
        for i in config: 
            if len(i) > 16:
                
                if mode == 'scamp':
                    string = i.ljust(24) + ''
                else:
                    print('Config parameter name len bigger than 16 chars.')
                    string = i.ljust(17) + '\n' + ''.ljust(17)
            else:
                string = i.ljust(17)

            if len(str(config[i]['value'])) > 14:
                string = string + str(config[i]['value']).ljust(15) + '\n' + ''.ljust(17) + ''.ljust(15)
            else:
                string = string + str(config[i]['value']).ljust(15)

            string = string + '#' + str(config[i]['comment']) +'\n'
            string = string + '\n'

            file.write(string)

        file.close()
    
    def read_config(self, filename, overwrite_config=True):
        file = open(filename, 'r')

        f = file.read()
        config = {}
        for i in f.split('\n'):
            i = str(i)

            if len(i) > 1 and i[0] != ' ':
                if i[0] == '#':
                    continue

                if i[0] != ' ' and i[0] != '#' and i[0] != "\n" :
                    actual = i[0:17].strip()
                    config[actual] = {"value": '', "comment": ''}
                    i = i[17:].split('#')

                if len(i) > 1:
                    config[actual]['value'] = i[0].strip()
                    config[actual]['comment'] = i[1].strip()
                else:
                    config[actual]['value'] = i[0].strip()

                continue

            if len(i) > 1 and i.split('#')[0][0] == ' ':
                if len(i.split('#')[1]) > 1:
                    config[actual]['comment'] = i.split('#')[1]
        
        if overwrite_config:
            self.config = config
        else:
            for i in config:
                self.config[i]['value'] = config[i]['value']
    
    def write_params(self):
        file = open(os.path.join(self.path, 'params.sex') , 'w')
        for i in self.params:
            file.write(i + '\n')
        
        file.close()
            
    
    def convert(self, dicti=None):
        '''
            From Normal dict to dict with values and comments
        '''
        
        if dicti is None:
            nconf = {}
            for i in self.config:
                nconf[i] = {"value": self.config[i], "comment": ""}
                
            self.config = nconf
        else:
            nconf = {}
            for i in dicti:
                nconf[i] = {"value": dicti[i], "comment": ""}
                
            return nconf