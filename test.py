import hashlib

username = input("Enter Username:")
password = input("Enter Password:")
auth_hash = hashlib.md5(password.encode()).hexdigest()

with open("credentials.txt", "w") as f:
	f.write(username+" "+auth_hash)
f.close()




