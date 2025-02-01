import memory_graph as mg

mg_visualization_status = False
print('running:', __file__)
print('Call mg_switch() to turn on/off auto memory_graph visualization.')

def mg_visualization(execution_result):
    ipython_locals = get_ipython().user_ns
    mg.show(mg.ipython_locals_filter(ipython_locals))

def mg_switch():
    global mg_visualization_status
    mg_visualization_status = not mg_visualization_status
    if mg_visualization_status:
        get_ipython().events.register("post_run_cell", mg_visualization)
    else:
        get_ipython().events.unregister("post_run_cell", mg_visualization)
    return mg_visualization_status
