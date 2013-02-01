define [
    'jquery'
], ($) ->
    getCookie = (name) ->
        if document.cookie && document.cookie != ''
            for cookie in document.cookie.split ';'
                if $.trim(cookie)[0..name.length] == "#{name}="
                    return decodeURIComponent cookie[name.length + 1..]
        return null

    getCookie


