from main_utils import *

welcome_message()

validation = -1
while (validation == -1):
    t_opt = task_options()
    t_opt = to_string(t_opt)
    t_opt = to_lowercase(t_opt)
    validation = check_task_option(t_opt)

