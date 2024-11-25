import bcrypt, jwt, os
from typing import Union, Optional
from datetime import datetime, timedelta

def hash_pwd(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def generate_token(
    data: dict,
    exp: Optional[bool] = False,
    duration: Optional[int] = None,
    refresh: Optional[bool] = False,
) -> Union[str, bool]:
    try:
        token = None
        if exp and refresh:
            to_encode = data.copy()
            days = (
                int(duration)
                if duration
                else int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 1))
            )
            exp = datetime.now() + timedelta(days=days)
            to_encode.update({"exp": exp})
            token = jwt.encode(
                to_encode,
                os.getenv("JWT_SECRET"),
                algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            )

        elif exp and not refresh:
            to_encode = data.copy()
            days = (
                int(duration)
                if duration
                else int(os.environ.get("JWT_TOKEN_EXPIRES", 1))
            )
            exp = datetime.now() + timedelta(days=days)
            to_encode.update({"exp": exp})
            token = jwt.encode(
                to_encode,
                os.getenv("JWT_SECRET"),
                algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            )
        else:
            token = jwt.encode(
                data,
                os.getenv("JWT_SECRET"),
                algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            )
        return token
    except Exception as error:
        print(f"an error occured when generating token: {error}")
        return None
    
def decode_token(token: str) -> Union[dict, bool]:
    try:
        data = jwt.decode(
            token,
            os.environ.get("JWT_SECRET"),
            algorithms=[os.environ.get("JWT_ALGORITHM", "HS256")],
        )
        return data
    except jwt.DecodeError:
        return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False