import json
import numpy as np

def module_fit(x, a,b,c,d,e,f,g,h,i,j,k):
    return a/(x**2) + b / x +c*x**0.5 +  d*x + e*x**2 + f*x**3 + g*x**0.5*np.log(x) + h*x*np.log(x) + i*x**2*np.log(x) + j*np.log(x) + k

def fit_pre(fit_parameter_path, preprocs):
    fit_parameter = json.load(open(fit_parameter_path,'r'))
    modules = list(preprocs.keys())
    procs = list(preprocs.values())

    lenmodules = len(modules)
    result = {}
    for i in range(lenmodules):
        module_data = fit_parameter[modules[i]]
        module_parameter = []
        min_down = 9999
        max_up = 0
        min_key = "a"
        max_key = "b"
        for key in module_data:
            # if module_data[key]["down"] >= procs[i]:
                # module_parameter=module_data[key]["parameter"]
            if module_data[key]["down"] < min_down:
                min_down = module_data[key]["down"]
                min_key = key
            if  module_data[key]["up"] > max_up:
                max_up =  module_data[key]["up"] 
                max_key = key
            if module_data[key]["down"] <= procs[i] and  module_data[key]["up"] > procs[i]:
                module_parameter=module_data[key]["parameter"]
            # elif module_data[key]["up"] <= procs[i]:
                # module_parameter=module_data[key]["parameter"]
        if not module_parameter:
            if procs[i] < min_down:
                module_parameter = module_data[min_key]["parameter"]
            elif procs[i] > max_up:
                module_parameter = module_data[max_key]["parameter"]
            else:
                print("error parameter!")
                return
        result[modules[i]] = module_fit(procs[i], module_parameter[0],module_parameter[1],module_parameter[2],module_parameter[3],module_parameter[4],module_parameter[5],module_parameter[6],module_parameter[7],module_parameter[8],module_parameter[9],module_parameter[10])
    return result

fit_parameter_path="/data/wujx01/EARthLab_UQ/TaskOptimize_FunLayer/db_test/fit_parameters.json.B"
preprocs={}
preprocs["atm"] = 127
preprocs["lnd"] =128
preprocs["ice"] =128
preprocs["ocn"] =128
preprocs["cpl"] =128
preprocs["cplatm"] =64
preprocs["cpllnd"] =128
preprocs["cplice"] =128
preprocs["cplocn"] =128
preprocs["none"] =128

pre_result = fit_pre(fit_parameter_path, preprocs)
print(pre_result)