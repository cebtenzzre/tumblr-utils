import importlib.resources
from abc import ABC, abstractmethod
from typing import Any, Literal, TypeVar

from pydantic import BaseModel, TypeAdapter
from typing_extensions import override

from .models import ContentBlockList, Options, _content_block_list_adapter

__all__ = [
    'MiniRacerNpfRenderer',
    'NpfRenderer',
    'QuickJsNpfRenderer',
]

T = TypeVar('T')

BUNDLE_PATH = '../assets/npf2html.iife.js'


def dump_js(model: BaseModel) -> Any:
    """Dump a Pydantic model with parameters suitable for passing to JavaScript."""
    return model.model_dump(mode='json', by_alias=True, exclude_none=True)


def dump_js_adapter(adapter: TypeAdapter[T], model: T) -> Any:
    """Dump a Python object with parameters suitable for passing to JavaScript."""
    return adapter.dump_python(model, mode='json', by_alias=True, exclude_none=True)


try:
    import quickjs
    have_quickjs = True
except ImportError:
    have_quickjs = False

try:
    from py_mini_racer import MiniRacer
    have_miniracer = True
except ImportError:
    have_miniracer = False


class NpfRenderer(ABC):
    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    @classmethod
    @abstractmethod
    def available(cls) -> bool: ...

    @abstractmethod
    def __call__(self, blocks: ContentBlockList, options: Options | None = None) -> str: ...

    def _load_bundle(self) -> str:
        return importlib.resources.files(__package__).joinpath(BUNDLE_PATH).read_text(encoding='utf-8')


class QuickJsNpfRenderer(NpfRenderer):
    @override
    @classmethod
    def name(cls) -> Literal['quickjs']:
        return 'quickjs'

    @override
    @classmethod
    def available(cls) -> bool:
        return have_quickjs

    def __init__(self) -> None:
        if not self.available():
            raise RuntimeError('Cannot instantiate QuickJsNpfRenderer: quickjs not available')
        code = self._load_bundle()
        code += '\nglobalThis.render = npf2html.default;'
        self.func = quickjs.Function('render', code)

    def __call__(self, blocks: ContentBlockList, options: Options | None = None) -> str:
        args = [dump_js_adapter(_content_block_list_adapter, blocks)]
        if options is not None:
            args.append(dump_js(options))
        return self.func(*args)


class MiniRacerNpfRenderer(NpfRenderer):
    @override
    @classmethod
    def name(cls) -> Literal['mini-racer']:
        return 'mini-racer'

    @override
    @classmethod
    def available(cls) -> bool:
        return have_miniracer

    def __init__(self) -> None:
        if not self.available():
            raise RuntimeError('Cannot instantiate MiniRacerNpfRenderer: mini-racer not available')
        self.ctx = MiniRacer()
        self.ctx.eval(self._load_bundle())

    def __call__(self, blocks: ContentBlockList, options: Options | None = None) -> str:
        args = [dump_js_adapter(_content_block_list_adapter, blocks)]
        if options is not None:
            args.append(dump_js(options))
        return self.ctx.call('npf2html.default', *args)


def create_npf_renderer() -> NpfRenderer | None:
    for cls in [
        QuickJsNpfRenderer,  # preferred
        MiniRacerNpfRenderer,
    ]:
        if cls.available():
            return cls()

    return None
