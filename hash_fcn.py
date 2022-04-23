# https://docs.python.org/3/library/hashlib.html

# salt: randomly generated data to fill the pw
# iter: The number of iterations should be chosen based on the hash algorithm and computing power. 
        # As of 2022, hundreds of thousands of iterations of SHA-256 are suggested
# hmac as pseudo random fcn
# hash digest algorithm for HMAC - sha256
# password and salt are input as bytes


from hashlib import pbkdf2_hmac
iter = 500_000  
hash = pbkdf2_hmac('sha256', b'1234', b'salt'*2, iter)
hash.hex()


# Write and print for testing purposes
with open('output.txt', "w") as output_f:
    output_f.write(hash.hex())

print(hash.hex())