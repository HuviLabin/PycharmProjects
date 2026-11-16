import bcrypt


def hash_password(password: str) -> str:
    # המרת המחרוזת לבייטים (bytes) כפי שאלגוריתם bcrypt דורש
    pwd_bytes = password.encode('utf-8')
    # יצירת Salt (תוספת אקראית לחיזוק האבטחה) וביצוע הגיבוב
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # החזרת התוצאה כמחרוזת רגילה (str) כדי שניתן יהיה לשמור אותה במסד הנתונים
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # המרת שתי המחרוזות לבייטים לצורך ההשוואה
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    # בדיקה האם הסיסמה הרגילה תואמת לגיבוב השמור
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)
