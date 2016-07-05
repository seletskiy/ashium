py import ashium

augroup ashium
    au!
    au BufReadPost /tmp*/ash.*/* py ashium.try_to_load_from_current_file()
    au FileType diff
            \ syn match DiffComment "^#.*" containedin=ALL |
            \ syn match DiffCommentIgnore "^###.*" containedin=DiffComment |
            \ syn match DiffAdded "\(^###.*\s\)\@<=A" containedin=DiffCommentIgnore |
            \ syn match DiffChanged "\(^###.*\s\)\@<=M" containedin=DiffCommentIgnore |
            \ syn match DiffChanged "\(^###.*\s\)\@<=R" containedin=DiffCommentIgnore |
            \ syn match DiffRemoved "\(^###.*\s\)\@<=D" containedin=DiffCommentIgnore |
            \ syn match DiffCommentIgnore "^###.*" containedin=DiffComment |
            \ syn match DiffInfo "^---.*" containedin=ALL |
            \ syn match DiffInfo "^+++.*" containedin=ALL |
            \ syn match DiffInfo "^@@ .*" containedin=ALL |
            \ syn match DiffAdded "^+.*" containedin=ALL |
            \ syn match DiffRemoved "^-.*" containedin=ALL |
            \ syn match DiffContext "^ " containedin=ALL |
            \ hi link DiffCommentAdded DiffAdded |
            \ hi link DiffCommentChanged DiffChanged |
            \ hi link DiffCommentRemoved DiffRemoved
augroup END
