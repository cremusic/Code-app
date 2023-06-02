"""Script to generate password hash"""
from getpass import getpass
from passlib.hash import pbkdf2_sha256


def validate_pwd_policy(password: str) -> tuple[bool, str]:
    """Validate password policy:
        - At least 8 characters
        - At least 1 uppercase character
        - At least 1 lowercase character
        - At least 1 digit
        - At least 1 special character
        - No whitespaces
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least 1 uppercase character"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least 1 lowercase character"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least 1 digit"

    special_chars = "!@#$%^&*()-_=+,.?/:;{}[]`~"
    if not any(c in special_chars for c in password):
        return (
            False,
            "Password must contain at least 1 special character: " + special_chars
        )

    if any(c.isspace() for c in password):
        return False, "Password must not contain any whitespaces"

    return True, ""


def main():
    password = getpass("Password: ")
    password_confirm = getpass("Confirm password: ")
    if password != password_confirm:
        print("Passwords do not match")
        return
    valid, msg = validate_pwd_policy(password)
    if not valid:
        print(msg)
        return
    print(
        "Password hash:",
        pbkdf2_sha256.hash(password)
    )


if __name__ == "__main__":
    main()
