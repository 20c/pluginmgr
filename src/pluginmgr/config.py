import collections

import munge.util

import pluginmgr


class PluginBase:
    """
    Example base class for plugins, set config and call init()
    """

    def __init__(self, config):
        # XXX document - pluginmgr_config is required
        self.pluginmgr_config = config
        self.init()

    def init(self):
        """
        called after the plugin is initialized, plugin may define this for any
        other initialization code
        """
        pass


class ConfigPluginManager(pluginmgr.PluginManager):
    """
    Plugin manager class that also handles config objects
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instance = {}

    def _ctor(self, typ, config, *args, **kwargs):
        self.log.debug(
            f"ctor: self._instance={self._instance} self._class={self._class}"
        )
        if typ in self._instance:
            # get class type, copy config, override with passed config
            obj = self._instance[typ]
            cp = obj.pluginmgr_config.copy()
            munge.util.recursive_update(cp, config)
            return type(obj)(cp, *args, **kwargs)
        # try to load
        return self.get_plugin_class(typ)(config, *args, **kwargs)

    def new_plugin(self, config, *args, **kwargs):
        """
        instantiate a plugin
        creates the object, stores it in _instance
        """
        typ = None
        obj = None

        # if type is defined, create a new instance
        if "type" in config:
            typ = config["type"]

        # single key is overriding an existing plugin instance
        elif isinstance(config, collections.Mapping) and len(config) == 1:
            # get type name and shift out config to parent level
            (typ, config) = list(config.items())[0]

        obj = self._ctor(typ, config, *args, **kwargs)

        # store if named
        if "name" in config:
            self._instance[config["name"]] = obj
        else:
            # this could dupe on .name, make name=''?
            config["name"] = typ

        return obj

    def get_instance(self, node, *args, **kwargs):
        """
        get plugin instance from config node
        *NOTE* returns an uninitialized instance if one isn't there
        *NOTE* instantiated plugins without names remain anonymous
               FIXME - why would instantiate() even process them
        """
        # string is a ref to an existing plugin instance
        if isinstance(node, str):
            if node in self._instance:
                return self._instance[node]
            # if not an instance, try for init with empty config
            return self.new_plugin({"type": node}, *args, **kwargs)

        if isinstance(node, collections.Mapping):
            if "type" in node:
                # node was a plugin config passed directly
                name = node.get("name", node.get("type"))
            elif len(node) == 1:
                # node was a container with a single plugin config keyed
                # to it
                typ, config = list(node.items())[0]
                name = config.get("name", config.get("type", typ))

            # retrieve existing instance if it exists
            if name in self._instance:
                return self._instance[name]

            # otherwise spawn new plugin
            return self.new_plugin(node, *args, **kwargs)

        raise ValueError(f"unable to parse plugin for output {node}")

    def instantiate(self, config, *args, **kwargs):
        """
        takes plugin config (list under 'plugin') and instantiates defined
        plugins
        """
        for plugin_config in config:
            self.new_plugin(plugin_config, *args, **kwargs)
