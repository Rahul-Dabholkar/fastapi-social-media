from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hashing the password
def hash(password: str):
    return pwd_context.hash(password)


# comparing hashed password when logging in
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
