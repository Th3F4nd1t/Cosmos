"""
DEPRECATED: This module is deprecated and will be removed in favor of a new implementation that handles multiple remote shell instances.
"""


# from tools.terminal.decorators import user_run, system_run

# class CommandContext:
#     @system_run
#     def __init__(self, name, commands=None):
#         self.name = name
#         self.commands = commands or {}
#         self.parent = None  # For going "up"

#     @system_run
#     def add_command(self, name, func_or_ctx):
#         self.commands[name] = func_or_ctx

#     @system_run
#     def run_command(self, command, args):
#         if command in self.commands:
#             cmd = self.commands[command]
#             if isinstance(cmd, CommandContext):
#                 cmd.parent = self
#                 return cmd  # Switch context
#             else:
#                 cmd(args)  # Run the function
#         elif command == 'exit':
#             return self.parent or self
#         else:
#             print(f"Unknown command: {command}")
#         return self

# @system_run
# def shell_loop(root_context):
#     current = root_context
#     while True:
#         path = []
#         ctx = current
#         while ctx:
#             path.append(ctx.name)
#             ctx = ctx.parent
#         prompt = ">".join(reversed(path)) + "> "
#         try:
#             user_input = input(prompt).strip()
#         except (EOFError, KeyboardInterrupt):
#             # print("\nBye.")
#             # break
#             print("\nUse `stop` to stop the FMS shell.")

#         if not user_input:
#             continue

#         parts = user_input.split()
#         command = parts[0]
#         args = parts[1:]

#         current = current.run_command(command, args)