def hello_world():
    print("Hello, world!")

def check_type(data):
    if isinstance(data, dict):
        return "It's a dictionary"
    elif isinstance(data, list):
        return "It's a list"
    else:
        return "Unknown type"

if __name__ == "__main__":
    hello_world()
    result = check_type({"key": "value"})
    print(result)