# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

class call_stack(dict):
    """Inherits from dict to give the call stack it own name and color. """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
