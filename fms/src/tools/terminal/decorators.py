import inspect
import ast
import functools

#### Decorator functions for user and system runs


def user_run(func):
    sig = inspect.signature(func)
    if 'instance_id' not in sig.parameters:
        raise TypeError(f"@user_run function '{func.__name__}' must have an 'instance_id' argument.")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def system_run(func):
    sig = inspect.signature(func)
    if 'instance_id' in sig.parameters:
        raise TypeError(f"@system_run function '{func.__name__}' cannot have an 'instance_id' argument.")

    # # Parse source code and check for send_message()
    # try:
    #     source = inspect.getsource(func)
    #     parsed = ast.parse(source)
    # except OSError:
    #     raise RuntimeError(f"Couldn’t read source for function '{func.__name__}'. Probably doing something shady.")

    # class NoSendMessage(ast.NodeVisitor):
    #     def visit_Call(self, node):
    #         if isinstance(node.func, ast.Name) and node.func.id == 'send_message':
    #             raise RuntimeError(f"@system_run function '{func.__name__}' is not allowed to call send_message(). Naughty.")
    #         self.generic_visit(node)

    # NoSendMessage().visit(parsed)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper