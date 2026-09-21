
def log_call(function):  # decorator example
    def wrapper(*args, **kwargs):
        print(f"log: '{function.__name__}' called with: {args}, {kwargs}")
        return_value = function(*args, **kwargs)
        print(f"log: '{function.__name__}' returned with: {return_value}")
        return return_value
    return wrapper

@log_call
def calculate_total(price, quantity, rounding=False):
    result = price * quantity
    return round(result) if rounding else result

@log_call
def send_email(receiver, message, sender="support@company.com"):
    print(f"Sending email to:{receiver} from:{sender}, {message}")

total = calculate_total(7.5, 3, rounding=True)
print(total)
send_email("alice@example.com", "Your order is ready")
