import imp
import importlib
import logging
import os
import re
import sys

import pkg_resources


class SearchPathImporter:
    """
    import hook to dynamically load modules from a search path

    """

    def __init__(self, namespace, searchpath, create_loader):
        self._searchpath = []
        self.package = namespace.split(".")[0]
        self.namespace = namespace
        self.log = logging.getLogger(__name__)
        self.re_ns = re.compile(r"^%s\.(.*)$" % re.escape(self.namespace))
        self.log.debug(f"hook.compile({self.namespace})")
        self.searchpath = searchpath
        self.create_loader = create_loader

    @property
    def searchpath(self):
        return getattr(self, "_searchpath")

    @searchpath.setter
    def searchpath(self, value):
        if not value:
            self._searchpath = []
        elif isinstance(value, str):
            self._searchpath = [value]
        else:
            self._searchpath = [x for x in value if x]

    # import hooks
    def find_module(self, fullname, path=None):
        self.log.debug(f"hook.namespace {self.namespace}")
        self.log.debug(f"hook.find({fullname}, {path}) loader={self.create_loader}")
        if self.create_loader:
            # trying to import package level creates an infinite loop
            if fullname == self.package:
                return self
            if fullname == self.namespace:
                return self

        match = self.re_ns.match(fullname)
        self.log.debug(f"match {match}")

        if not match:
            return

        name = match.group(1)
        self.log.debug(f"hook match {name}")
        if self.find_file(name):
            return self

    def find_file(self, name):
        for each in self.searchpath:
            fq_path = os.path.join(each, name + ".py")
            self.log.debug(f"checking {fq_path}")
            if os.path.isfile(fq_path):
                return fq_path

    def load_module(self, fullname):
        self.log.debug(f"hook.load({fullname})")

        # build package for loader if it doesn't exist
        # don't need to check for create_loader here, checks in find_module
        if fullname == self.package or fullname == self.namespace:
            self.log.debug(f"hook.create_loader({fullname})")
            # make a new loader module
            mod = imp.new_module(fullname)

            # set a few properties required by PEP 302
            mod.__file__ = self.namespace
            mod.__name__ = fullname
            mod.__path__ = self.searchpath
            mod.__loader__ = self
            mod.__package__ = ".".join(fullname.split(".")[:-1])
            sys.modules[fullname] = mod
            return mod

        match = self.re_ns.match(fullname)
        self.log.debug(f"match {match}")

        if not match:
            raise ImportError(fullname)

        name = match.group(1)
        filename = self.find_file(name)
        if not filename:
            raise ImportError(fullname)
        self.log.debug(f"hook.found({filename})")

        try:
            loader = importlib.machinery.SourceFileLoader(fullname, filename)
            mod = loader.load_module()

        except Exception as exc:
            self.log.error(
                "failed loading %s, %s(%s)", name, exc.__class__.__name__, str(exc)
            )
            raise

        # don't need to check mod, both throw instead of returning None

        self.log.debug(f"hook.loaded({fullname}) - {mod}")
        sys.modules[fullname] = mod
        return mod


class PluginManager:
    def __init__(self, namespace, searchpath=None, create_loader=False):
        """
        namespace: import from (what you would type after `import`)
        searchpath: a directory or list of directories to search in
        create_loader: determines if this should create a blank loader to
                      import through. This should be enabled if there isn't
                      a real module path for the namespace and disabled for
                      sharing the namespace with static modules
        """
        self._class = {}
        self._imphook = None
        self.log = logging.getLogger(__name__)
        self.namespace = namespace
        self.create_loader = create_loader
        self.searchpath = searchpath

    @property
    def searchpath(self):
        if self._imphook:
            return self._imphook.searchpath
        return None

    @searchpath.setter
    def searchpath(self, value):
        if self._imphook:
            self._imphook.searchpath = value
            return

        if not value:
            return

        self._imphook = SearchPathImporter(self.namespace, value, self.create_loader)
        sys.meta_path.append(self._imphook)

    def import_external(self, namespace=None):
        if not namespace:
            namespace = self.namespace
        for entry_point in pkg_resources.iter_entry_points(namespace):
            module = entry_point.load()
            self.searchpath = (self.searchpath or []) + [
                os.path.dirname(module.__file__)
            ]
            # need to mark new searchpath as already imported
            # to avoid re-import from new namespace
            sys.modules[f"{namespace}{entry_point.name}"] = sys.modules[
                entry_point.module_name
            ]

    def register(self, typ):
        """ register a plugin """
        # should be able to combine class/instance namespace, and inherit from either
        # would need to store meta or rely on copy ctor
        def _func(cls):
            if typ in self._class:
                raise ValueError("duplicated type name '%s'" % typ)
            cls.plugin_type = typ
            self._class[typ] = cls
            return cls

        return _func

    @property
    def registry(self):
        """
        class dictionary of name: class
        """
        return self._class.copy()

    def get_plugin_class(self, typ):
        """
        get class by name
        """
        if typ in self._class:
            return self._class[typ]

        # try to import by same name
        try:
            importlib.import_module(f"{self.namespace}.{typ}")
            if typ in self._class:
                return self._class[typ]

        except ImportError as exc:
            self.log.debug(f"ImportError {exc}")

        raise ValueError(f"unknown plugin '{typ}'")
