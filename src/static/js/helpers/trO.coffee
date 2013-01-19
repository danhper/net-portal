define [
    'handlebars'
    'i18next'
], (Handlebars, i18next) ->
    trO = (object, arg) ->
        currentLng = i18next.lng()
        fallback = i18next.options.fallbackLng
        if "#{currentLng}_#{arg}" in object
            val = object["#{currentLng}_#{arg}"]
        else if "#{fallback}_#{arg}" in object
            val = object["#{fallback}_#{arg}"]
        else
            throw "No key #{arg} for local #{currentLng} in given object"

        new Handlebars.SafeString(val)

    Handlebars.registerHelper('trO', trO)
    trO
