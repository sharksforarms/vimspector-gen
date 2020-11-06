# vimspector-gen

This plugin can be used to generate/update a `.vimspector.json` file with your targets.

## Installation

### vim-plug

```VimL
Plug 'sharksforarms/vimspector-gen'
```

`:UpdateRemotePlugins` will need to be called after installation
to load the plugin

## Functions

This plugin exposes the following functions

```VimL
" Creates the .vimspector.json file
:VimspectorGenerateNew <lang>

" Updates the .vimspector.json file
:VimspectorGenerateUpdate <lang>
```

## Supported Languages

| Language |
|----------|
| rust     |

