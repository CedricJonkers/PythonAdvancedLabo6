class InputHandler:
    @staticmethod
    def handle_numeric_choice(prompt, max_choice, error_message):
        while True:
            user_input = input(prompt)
            try:
                choice = int(user_input)
                if 1 <= choice <= max_choice:
                    return choice
                else:
                    print(error_message)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def handle_string_input(prompt, validation_func, error_message):
        while True:
            user_input = input(prompt)
            try:
                if validation_func(user_input):
                    return user_input
                else:
                    print(error_message)
            except Exception as e:
                print(f"An error occurred: {e}")