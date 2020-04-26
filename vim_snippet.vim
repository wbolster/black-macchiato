function! s:RunBlackMacchiato() range
    let cmd = "black-macchiato"
    if !executable(cmd)
        echohl ErrorMsg
        echom "black-macchiato not found!"
        echohl None
        return
    endif

    silent execute a:firstline . "," . a:lastline."!" . cmd

    echo "Done formatting."

endfunction

" Create a command to call the black-macchiato function
command -range BlackMacchiato <line1>,<line2>call <sid>RunBlackMacchiato()

" Optionally add keyboard shortcuts to call the command in normal and visual modes
autocmd FileType python xnoremap <buffer> <Leader>f :'<,'>BlackMacchiato<cr>
autocmd FileType python nnoremap <buffer> <Leader>f :BlackMacchiato<cr>
