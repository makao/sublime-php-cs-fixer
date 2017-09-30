# Sublime PHP CS Fixer

This Sublime Text 3 Package provides interface for [PHP Coding Standards Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)

## Installation
First make sure that PHP-CS-Fixer is installed. This plugin is compatible with v2. For more information visit [PHP-CS-Fixer website](http://cs.sensiolabs.org)
### Package control
Not available
### Manual installation
Clone this repository into `{packages directory}/PHPCSFixer`.
You can find it using Sublime menu: <kbd>Preferences</kbd> > <kbd>Browse Packages</kbd>

## Commands
There aren't any keybindings included, but you can simply bind command yourself.

### php_cs_fixer_fix
Fixes active file

## Settings

Settings have 3 scopes: default, user and project. Default should not be changed.
Settings can be accessed via <kbd>Preferences</kbd> > <kbd>Package Settings</kbd> > <kbd>PHP-CS-Fixer</kbd> > <kbd>Settings</kbd>

If you want to configure this plugin for project you can create `php-cs-fixer` entry in `.sublime-project` file:
```
{
    "folders":
    [
        {
            "path": "."
        }
    ],
    "settings":
    {
        "php-cs-fixer": {
            "ignored_extensions": [".phtml"],
            "on_save": true,
            "rules": ["@PSR2,no_unused_imports,trailing_comma_in_multiline_array"],
        }
    }
}
```

### executable
Executable path.

### ignored_extensions
Ignored filename endings, useful when using templating system where fixing could produce unpredictable output.

### on_save
Automatically fix file on save.

### rules
List of rules applied to fixer. [List of all rules available here](http://cs.sensiolabs.org/#usage).

## TODO
- Handling .phpcs configuration file

## Credits
This plugin was inspired by [GitGutter plugin](https://github.com/jisaacks/GitGutter), [sublime-phpcs](http://benmatselby.github.io/sublime-phpcs/) and [PHP-CS-Fixer](http://cs.sensiolabs.org).
