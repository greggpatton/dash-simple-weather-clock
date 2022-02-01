import base64


def encode(data: str) -> str:
    data_str = data

    if not type(data_str) is str:
        data_str = str(data_str)

    # String to bytes
    b = bytes(data_str, "utf-8")

    # Bytes to base64
    b64encoded = base64.urlsafe_b64encode(b)

    # Base64 to string
    encoded = b64encoded.decode("utf-8")

    return encoded


def decode(data: str) -> str:
    data_str = data

    if not type(data_str) is str:
        data_str = str(data_str)

    # Base64 string to bytes
    decoded = data_str.encode("utf-8")

    try:
        # Base64 bytes to string
        decoded_str = base64.urlsafe_b64decode(decoded).decode("utf-8")
    except Exception as e:
        print(e)
        decoded_str = None

    return decoded_str


if __name__ == "__main__":

    class AClass(object):
        def hello(self):
            print(f"Hello World!  I am {self.__class__.__name__}")

    key = str(AClass)

    encoded_key = encode(key)
    print("encoded_key = ", type(encoded_key), "  ", encoded_key)

    decoded_key = decode(encoded_key)
    print("decoded_key = ", type(decoded_key), "  ", decoded_key)

    d = {str(AClass): AClass}

    d[decoded_key]().hello()
