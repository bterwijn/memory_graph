mg_visualization_status = False

try: # try-except fixes problem with 'spyder'
    import memory_graph as mg

    print('running:', __file__)
    print('Call mg_switch() to turn on/off auto memory_graph visualization.')

    def mg_visualization(execution_result):
        ipython_locals = get_ipython().user_ns
        mg.show(mg.ipython_locals_filter(ipython_locals))

    def mg_switch(status = None):
        global mg_visualization_status
        if isinstance(status, bool):
            mg_visualization_status = status
        else:
            mg_visualization_status = not mg_visualization_status
        if mg_visualization_status:
            get_ipython().events.register("post_run_cell", mg_visualization)
        else:
            get_ipython().events.unregister("post_run_cell", mg_visualization)
        return mg_visualization_status
except Exception as e:
    print(f"Failed to run auto_memory_graph.py: {e}")
