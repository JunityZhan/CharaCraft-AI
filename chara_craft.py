import argparse
from CharaCraft import generate, extract, animate, spider

class CharaCraft:
    def __init__(self):
        # Initialize a dictionary to hold the arguments for each function.
        self.args_dict = {'me': 'traveler', 'first_response': 'Nice to meet you.', 'prompt': 'default',
                          'dynamic': False, 'dialogue': False, 'num_context': 2}
        # add default values
    def update(self, **kwargs):
        self.args_dict.update(kwargs)
    def generate(self, function, **kwargs):
        self.args_dict['module'] = 'generate'
        self.args_dict['function'] = function
        self.args_dict.update(kwargs)
        self.run()

    def extract(self, function, **kwargs):
        self.args_dict['module'] = 'extract'
        self.args_dict['function'] = function
        self.args_dict.update(kwargs)
        self.run()

    def animate(self, function, **kwargs):
        self.args_dict['module'] = 'animate'
        self.args_dict['function'] = function
        self.args_dict.update(kwargs)
        self.run()

    def spider(self, function, **kwargs):
        self.args_dict['module'] = 'spider'
        self.args_dict['function'] = function
        self.args_dict.update(kwargs)
        self.run()

    def run(self):
        # Convert the argument dictionary to an argparse.Namespace equivalent
        args = argparse.Namespace(**self.args_dict)

        # Dynamically get the module and function to call
        try:
            module = globals()[args.module]
            function_to_call = getattr(module, args.function)
        except KeyError:
            print(f"Module {args.module} is not defined.")
            return
        except AttributeError:
            print(f"Function {args.function} is not available in module {args.module}.")
            return

        function_to_call(args)

        # Reset the arguments dictionary for the next operation
