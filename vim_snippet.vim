function! s:RunBlackMacchiato(visual) range
    let cmd = "black-macchiato"
    if !executable(cmd)
        echo "black-macchiato not found!"
        return
    endif

    if a:visual
        normal! gv
    endif

    let currentMode = mode()

    if currentMode ==# "n"
        silent execute ".!" . cmd
    elseif currentMode ==# "v" || currentMode ==# "V"
        silent execute "'<,'>!" . cmd
    endif

    echo "Done formatting."

endfunction

autocmd FileType python xnoremap <buffer> <Leader>f :call <sid>RunBlackMacchiato(1)<cr>
autocmd FileType python nnoremap <buffer> <Leader>f :call <sid>RunBlackMacchiato(0)<cr>
