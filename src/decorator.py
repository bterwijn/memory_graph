def log_call(function):
    def wrapper(*args, **kwargs):
        print(f"Calling {function.__name__} with: {args}, {kwargs}")
        return_value = function(*args, **kwargs)
        print(f"Finished {function.__name__} with return value: {returned}")
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
