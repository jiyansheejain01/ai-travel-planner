from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

password = "MySecurePassword123"

hashed = hash_password(password)

print("Hash:", hashed)
print("Password Correct:", verify_password(password, hashed))
print("Password Wrong:", verify_password("wrongpassword", hashed))

print()

access_token = create_access_token("user-123")
refresh_token = create_refresh_token("user-123")

print("Access Token:")
print(access_token)

print()

print("Refresh Token:")
print(refresh_token)

print()

print("Decoded Access:")
print(decode_token(access_token))

print()

print("Decoded Refresh:")
print(decode_token(refresh_token))