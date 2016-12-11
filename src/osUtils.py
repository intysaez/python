
'''
    Author zombie(c) 2016
    A sample program for update python program dynamically
    Python Class, Fall C 2016
'''

import _ast
import copy
#we have to change the directory accoring to our
chDir = '/media/inty/Data'

source_code ="""
import geo

for file in os.listdir('.'):
    print(file)
    """

ast = compile(source_code, '<string>', 'exec', _ast.PyCF_ONLY_AST)
#After making connection it will scan deeply with root code and copy the all data with in the policies
astCopy = copy.deepcopy(ast)

os_import = copy.deepcopy(ast.body[0])
os_import.names[0].name = 'os'

ast.body.remove(ast.body[0])
ast.body.insert(0, os_import)

for_obj = ast.body[1]
for_obj.iter.args[0].s = chDir

#compling the code
code = compile(ast, '<string>', 'exec')

exec (code)


