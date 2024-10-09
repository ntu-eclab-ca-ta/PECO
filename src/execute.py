import subprocess

import variable

def for_all_commands(result):
    return True

def without_fail(result):
    return result.returncode == 0

def default_logger(result):
    if isinstance(result, str):
        return {'system': result}
    else:
        return {'stdout': result.stdout, 'stderr': result.stderr}

def execute_commands(config, field, logger = default_logger, is_success = without_fail):
    commands = config[field]['commands']
    timeout = config[field]['timeout'] if 'timeout' in config[field] else None
    log = []
    for command in commands:
        command = variable.solve_string(config, command)
        try:
            result = subprocess.run(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        except subprocess.TimeoutExpired:
            log.append({command: logger("Timeout")})
            return (log, False)

        log.append({command: logger(result)})
        if not is_success(result):
            return (log, False)
    return (log, True)