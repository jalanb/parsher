import unittest
from parsher import BashScript

class TestMultipleTokens(unittest.TestCase):
    def prep(self, string):
        path = './test_data'
        f = open(path, 'w')
        f.write(string)
        f.close()
        return BashScript(path)

    def test_simple_token(self):
        string = "somecommand"
        bashScript = self.prep(string)
        self.assertEquals([string], bashScript.commands)

    def test_multiple_tokens(self):
        string = "somecommand some@arg.with/symbols/foo.bar"
        bashScript = self.prep(string)
        self.assertEquals([string], bashScript.commands)

    def test_variable_assignment_no_command(self):
        string = "VAR=VALUE"
        bashScript = self.prep(string)
        self.assertEquals([string.split('=')], bashScript.vars)

    def test_variable_export(self):
        string = "export VAR=VALUE"
        bashScript = self.prep(string)
        self.assertEquals([['VAR', 'VALUE']], bashScript.vars)
        self.assertEquals('export', bashScript.commands[0])

    def test_variable_export_multiple(self):
        string = "export VAR1=VAL1\nexport VAR2=VAL2\nexport VAR3=VAL3"
        bashScript = self.prep(string)
        self.assertEquals([['VAR1', 'VAL1'], ['VAR2', 'VAL2'], ['VAR3', 'VAL3']], bashScript.vars)
        self.assertEquals(['export', 'export', 'export'], bashScript.commands)

    def test_variable_export_mutliple_with_command(self):
        string = "export VAR1=VAL1\nexport VAR2=VAL2\nexport VAR3=VAL3\nSomeCommand"
        bashScript = self.prep(string)
        self.assertEquals([['VAR1', 'VAL1'], ['VAR2', 'VAL2'], ['VAR3', 'VAL3']], bashScript.vars)
        self.assertEquals(['export', 'export', 'export', 'SomeCommand'], bashScript.commands)

    def test_variable_export_mutliple_with_command(self):
        string = "VAR1=VAL1 VAR2=VAL2 VAR3=VAL3 SomeCommand"
        bashScript = self.prep(string)
        self.assertEquals([['VAR1', 'VAL1'], ['VAR2', 'VAL2'], ['VAR3', 'VAL3']], bashScript.vars)
        self.assertEquals(['SomeCommand'], bashScript.commands)

    def test_semicolons_and_lstrip(self):
        string = "export VAR1=VAL1;; export VAR2=VAL2;\n\nexport VAR3=VAL3;SomeCommand"
        bashScript = self.prep(string)
        self.assertEquals([['VAR1', 'VAL1'], ['VAR2', 'VAL2'], ['VAR3', 'VAL3']], bashScript.vars)
        self.assertEquals(['export', 'export', 'export', 'SomeCommand'], bashScript.commands)



if __name__ == '__main__':
        unittest.main()


