

def run(in_params):
    outparams = {}

    if "p1" in in_params:
        outparams["resp"] = in_params["p1"]
    outparams["def"] = 'Hello world'
    return outparams