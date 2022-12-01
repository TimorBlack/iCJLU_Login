import hmac
import hashlib
def get_md5(password, token):
	return hmac.new(token.encode(), password.encode(), hashlib.md5).hexdigest()
if __name__ == '__main__':
	password = " "
	token = " "
	print(get_md5(password, token))