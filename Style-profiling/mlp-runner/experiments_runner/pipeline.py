from __future__ import annotations

import pathlib

from dataclasses import dataclass
from typing import Optional, Union, List, Callable


@dataclass
class Pipeline:
    pipeline_name: str
    pipeline_root: pathlib.Path
    components: List[Callable]

    def __init__(self,
                 name: str,
                 root: Optional[Union[str, pathlib.Path]] = None,
                 components: Optional[List[Callable]] = None) -> None:

        self.pipeline_name = str(name)

        #
        if root is None:
            root = ''
        self.pipeline_root = pathlib.Path(root)

        #
        if components is None:
            components = list()
        for i, c in enumerate(components):
            if not callable(c):
                raise TypeError(f'components should be list of callable, but: {c} @ {i}')
        self.components = components

    def __len__(self) -> int:
        return len(self.components)

    def append(self, component: Callable) -> Pipeline:

        if not callable(component):
            raise TypeError(f'component should be callable, but: {component}')

        self.components.append(component)
        return self

    def pop(self) -> Callable:
        return self.components.pop(0)
