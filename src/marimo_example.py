import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import memory_graph as mg
    import copy

    def custom_copy(a):
        c = a.copy()
        c[1] = a[1].copy()
        mg.show(mg.stack_marimo())
        breakpoint()
        return c

    a = [ [1, 2], ['x', 'y'] ]
    c1 = a
    c2 = copy.copy(a)
    c3 = custom_copy(a)
    c3 = copy.deepcopy(a)

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
