#!/usr/ccs/bin/vim
"==========================================="
" Filename: .vimrc
" Author: Peter Chang
" Jul 17, 2015
"==========================================="

"------------------ Vundle (Vim plugin manager) ------------------"

set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo

Plugin 'tpope/vim-fugitive'
Plugin 'Valloric/YouCompleteMe'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

"------------------ General ------------------"
" Use Vim settings, rather then Vi settings
" set nocompatible

" allow backspacing over everything in insert mode
set backspace=indent,eol,start

"Turn on the syntax
syn on

" scroll when the cursor is closed to the top or bottom
set scrolloff=15


" display a line at 81 columns
set colorcolumn=101
highlight ColorColumn ctermbg=8

"------------------ Search ------------------"
"Highlight the last search pattern"
set hlsearch

"Turn on instant search"
set nu incsearch

"When search in lower case, ignore the case. Otherwise be casesensitive
set ignorecase
set smartcase



"------------------ Tab/Indentation ------------------"
" 4 spaces for indenting
set shiftwidth=4

" Tab width is 4
set tabstop=4

" Spaces instead of tabs (disabled)
set expandtab

" Always  set auto indenting on
set autoindent

"------------------ Mouse ------------------"
" Use the mouse to move cursor
"set mouse=a

" Use mouse to edit text in insert mode (no copy)"
"set selectmode=mouse



"------------------ Command ------------------"
" set the commandheight
set cmdheight=2

" show (partial) commands
set showcmd



"------------------ Status Line ------------------"
" set status line
set statusline=[%02n]\ %f\ %(\[%M%R%H]%)%=\ %4l,%02c%2V\ %P%*

" Always display a status line at the bottom of the window
set laststatus=2

"------------------ theme ------------------"
colorscheme desert
if has("gui_running")
    syntax enable
    set background=dark
    colorscheme solarized
endif

" highlight current line
set cursorline
hi CursorLine term=bold cterm=bold guibg=Grey40

set tags+=./tags

" set paste

"------------------ YouCompleteMe ------------------"
let g:ycm_confirm_extra_conf = 0
" Code navigation with Ctrl-] , use Ctrl-O to get back to previous location
nnoremap <silent> <C-]> :YcmCompleter GoTo<CR>

command TrimWhiteSpace %s/\s\+$//
