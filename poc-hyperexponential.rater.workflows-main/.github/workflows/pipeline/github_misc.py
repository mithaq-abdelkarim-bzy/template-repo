import os

def set_output(name, value):
    if isinstance(value,str):
        value = value.replace("%", "")
        # value = value.replace("\n", " ")
        # value = value.replace("\r", " ")
        value = value.replace("\n", "\\n")
        value = value.replace("\r", "\\r")
        value = value.replace("'", "\\'")
    print('set_output', f'{name}={value}')
    out = os.getenv('GITHUB_OUTPUT', 'GITHUB_OUTPUT')
    with open(out, 'a') as fh:
        delimiter = "EOF"
        #print(f'{name}={value}', file=fh) #Does not support multiline strings. See print(f'{name}={value}', file=fh)
        print(f'{name}<<{delimiter}', file=fh)
        print(f'{value}', file=fh)
        print(f'{delimiter}', file=fh)