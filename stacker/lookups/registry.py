from ..exceptions import UnknownLookupType
from ..util import load_object_from_string

from .handlers import output
from .handlers import kms
from .handlers import xref
from .handlers import file as file_handler

LOOKUP_HANDLERS = {}
DEFAULT_LOOKUP = output.TYPE_NAME


def register_lookup_handler(lookup_type, handler_or_path):
    """Register a lookup handler.

    Args:
        lookup_type (str): Name to register the handler under
        handler_or_path (OneOf[func, str]): a function or a path to a handler

    """
    handler = handler_or_path
    if isinstance(handler_or_path, basestring):
        handler = load_object_from_string(handler_or_path)
    LOOKUP_HANDLERS[lookup_type] = handler


def resolve_lookups(lookups, context, provider):
    """Resolve a set of lookups.

    Args:
        lookups (list of :class:`stacker.lookups.Lookup`): a list of stacker
            lookups to resolve
        context (:class:`stacker.context.Context`): stacker context
        provider (:class:`stacker.provider.base.BaseProvider`): subclass of the
            base provider

    Returns:
        dict: dict of Lookup -> resolved value

    """
    resolved_lookups = {}
    for lookup in lookups:
        try:
            handler = LOOKUP_HANDLERS[lookup.type]
        except KeyError:
            raise UnknownLookupType(lookup)
        resolved_lookups[lookup] = handler(
            value=lookup.input,
            context=context,
            provider=provider,
        )
    return resolved_lookups

register_lookup_handler(output.TYPE_NAME, output.handler)
register_lookup_handler(kms.TYPE_NAME, kms.handler)
register_lookup_handler(xref.TYPE_NAME, xref.handler)
register_lookup_handler(file_handler.TYPE_NAME, file_handler.handler)
