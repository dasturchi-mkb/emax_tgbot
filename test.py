import certifi
import ssl

print(certifi.where())

ctx = ssl.create_default_context(cafile=certifi.where())
print(ctx)
