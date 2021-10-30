def propagate_args(common_args, resp):
    for key, val in common_args.items():
        if val is not None:
            resp[key] = val
    return resp
