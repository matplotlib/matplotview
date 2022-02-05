import functools

def _fix_super_reference(function):
    """
    Private utility decorator. Allows a function to be transferred to another
    class by dynamically updating the local __class__ attribute of the function
    when called. This allows for use of zero argument super in all methods

    Parameters:
    -----------
    function
        The function to wrap, to allow for the dynamic
    """
    @functools.wraps(function)
    def run_function(self, *args, **kwargs):
        try:
            cls_idx = function.__code__.co_freevars.index('__class__')
            old_value = function.__closure__[cls_idx].cell_contents
            function.__closure__[cls_idx].cell_contents = type(self)
            res = function(self, *args, **kwargs)
            function.__closure__[cls_idx].cell_contents = old_value
            return res
        except (AttributeError, ValueError):
            return function(self, *args, **kwargs)

    return run_function


class _WrappingType(type):
    def __new__(mcs, *args, **kwargs):
        res = super().__new__(mcs, *args, **kwargs)

        res.__base_wrapping__ = getattr(
            res, "__base_wrapping__", res.__bases__[0]
        )
        res.__instances__ = getattr(res, "__instances__", {})

        return res

    def __getitem__(cls, the_type):
        if(cls.__instances__ is None):
            raise TypeError("Already instantiated wrapper!")

        if(the_type == cls.__base_wrapping__):
            return cls

        if(issubclass(super().__class__, _WrappingType)):
            return cls._gen_type(super()[the_type])

        if(not issubclass(the_type, cls.__base_wrapping__)):
            raise TypeError(
                f"The extension type {the_type} must be a subclass of "
                f"{cls.__base_wrapping__}"
            )

        return cls._gen_type(the_type)

    def _gen_type(cls, the_type):
        if(the_type not in cls.__instances__):
            cls.__instances__[the_type] = _WrappingType(
                f"{cls.__name__}[{the_type.__name__}]",
                (the_type,),
                {"__instances__": None}
            )
            cls._copy_attrs_to(cls.__instances__[the_type])

        return cls.__instances__[the_type]

    def _copy_attrs_to(cls, other):
        dont_copy = {"__dict__", "__weakref__", "__instances__"}

        for k, v in cls.__dict__.items():
            if(k not in dont_copy):
                setattr(
                    other,
                    k,
                    _fix_super_reference(v) if(hasattr(v, "__code__")) else v
                )

        other.__instances__ = None

    def __iter__(cls):
        return NotImplemented
