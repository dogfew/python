message = [i for i in input('Enter your message: ')]
code = [ord(symbol) for symbol in message]
ekey = eval(input('Encrypting key: '))
encr = []
for number in code:
    encr.append(number ^ ekey)
encrypted_message = ''.join([chr(number) for number in encr])
print(f'Your encrypted message:\n{encrypted_message}')
decode = [ord(symbol) for symbol in encrypted_message]
decoded_message = []
dkey = eval(input('Enter your key for decrypting: '))
for symbol in decode:
    decoded_message.append(symbol ^ dkey)
output = ''.join([chr(i) for i in decoded_message])
print(f'Your decrypted message:\n{output}')
