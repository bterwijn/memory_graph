# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

"""Extension to add memory graph configuration for public Pandas values."""
import reprlib

from memory_graph.node_leaf import Node_Leaf
from memory_graph.node_table import Node_Table

import memory_graph.config as config
import memory_graph.config_default as config_default


def _display_value(value):
    """Keep object references, but display Pandas scalar values without internals."""
    import pandas as pd

    if value is pd.NA or value is pd.NaT:
        return str(value)
    if isinstance(value, (pd.Timestamp, pd.Timedelta, pd.Period, pd.Interval)):
        return str(value)
    return value


def _column_name(name, default="value"):
    return default if name is None else str(name)


def _dataframe_to_node(data):
    # Unlike .values, itertuples does not coerce all numeric columns to one dtype.
    return Node_Table(
        data,
        [[_display_value(value) for value in row]
         for row in data.itertuples(index=False, name=None)],
        col_names=[str(name) for name in data.columns],
        row_names=[str(name) for name in data.index],
    )


def _series_to_node(data):
    return Node_Table(
        data,
        [[_display_value(value)] for value in data.tolist()],
        col_names=[_column_name(data.name)],
        row_names=[str(name) for name in data.index],
    )


def _index_to_node(data):
    # Also handles RangeIndex, DatetimeIndex, TimedeltaIndex and PeriodIndex
    # through config's base-class lookup.
    return Node_Table(
        data,
        [[_display_value(value)] for value in data.tolist()],
        col_names=[_column_name(data.name)],
    )


def _multiindex_to_node(data):
    # Use the actual row labels, not .levels (which includes unused labels).
    return Node_Table(
        data,
        [[_display_value(value) for value in row] for row in data.tolist()],
        col_names=[_column_name(name, f"level_{i}")
                   for i, name in enumerate(data.names)],
    )


class _Categorical_Table(Node_Table):
    """Show values as a table, with category order as compact metadata."""

    def get_label(self, slices):
        data = self.get_data()
        return (super().get_label(slices)
                + f"\ncategories={reprlib.repr(data.categories.tolist())}"
                + f"\nordered={data.ordered}")


def _categorical_to_node(data):
    return _Categorical_Table(
        data,
        [[_display_value(value)] for value in data.tolist()],
        col_names=[_column_name(getattr(data, "name", None))],
    )


def _intervalindex_to_node(data):
    return Node_Table(
        data,
        [[_display_value(left), _display_value(right), data.closed]
         for left, right in zip(data.left.tolist(), data.right.tolist())],
        col_names=["left", "right", "closed"],
    )


def _scalar_to_node(data):
    return Node_Leaf(data, str(data))


def _pandas_types():
    """Keep optional Pandas imports inside the extension, as before."""
    import pandas as pd

    return {
        pd.DataFrame: (_dataframe_to_node, "olivedrab1", "#3a4d13"),
        pd.Series: (_series_to_node, "olivedrab2", "#3a4d13"),
        pd.Index: (_index_to_node, "olivedrab3", "#384d24"),
        pd.MultiIndex: (_multiindex_to_node, "palegreen2", "#244d32"),
        pd.CategoricalIndex: (_categorical_to_node, "darkseagreen2", "#324d39"),
        pd.Categorical: (_categorical_to_node, "darkseagreen2", "#324d39"),
        pd.IntervalIndex: (_intervalindex_to_node, "lightgoldenrod1", "#5c5125"),
        # IndexSlice is an instance, not a public class or a table. Obtain its
        # type from the public singleton instead of importing a private type.
        type(pd.IndexSlice): (
            lambda data: Node_Leaf(data, "pd.IndexSlice (slice helper)"),
            "lightsteelblue1", "#30465c",
        ),
        pd.Timestamp: (_scalar_to_node, "olivedrab2", "#3a4d13"),
        pd.Timedelta: (_scalar_to_node, "olivedrab2", "#3a4d13"),
        pd.Period: (_scalar_to_node, "olivedrab2", "#3a4d13"),
        pd.Interval: (_scalar_to_node, "lightgoldenrod1", "#5c5125"),
        type(pd.NA): (_scalar_to_node, "gray85", "#454545"),
        type(pd.NaT): (_scalar_to_node, "gray85", "#454545"),
    }


def extend_pandas():
    for data_type, (to_node, light, dark) in _pandas_types().items():
        config.type_to_node[data_type] = to_node
        config_default.type_to_color_light[data_type] = light
        config_default.type_to_color_dark[data_type] = dark
        config.type_to_color[data_type] = dark if config.color_mode_dark else light


def unextend_pandas():
    for data_type in _pandas_types():
        config.type_to_node.pop(data_type, None)
        config.type_to_color.pop(data_type, None)
        # Remove theme defaults too, so changing theme cannot re-enable colors.
        config_default.type_to_color_light.pop(data_type, None)
        config_default.type_to_color_dark.pop(data_type, None)
