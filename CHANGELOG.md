
# Change Log

## [Unreleased]
### Added
### Fixed
### Changed
### Deprecated
### Removed
### Security


## [0.5.0]
### Added
- py36 tests

### Changed
- moved config plugins into separate config.ConfigPluginManager class
- renamed plugin config attr to pluginmgr_config

### Removed
- name attr from ConfigPlugin objects
- args and kwargs from config.PluginBase


## [0.4.0]
### Added
- py3 support

### Fixed
- always use full module name in sys.modules

### Changed
- check searchpath for null values


## [0.3.0]
### Added
- allow changing searchpath after instantiation

### Fixed
fix import loop at package level


## [0.2.0]
### Added
- variadic arguments to plugin ctors

