define [
    'handlebars'
    'i18next'
], (Handlebars, i18next) ->
    trObj = (object, arg) ->
        currentLng = i18next.lng()
        fallback = i18next.options.fallbackLng
        if "#{currentLng}_#{arg}" of object
            val = object["#{currentLng}_#{arg}"]
        else if "#{fallback}_#{arg}" of object
            val = object["#{fallback}_#{arg}"]
        else
            throw "No key #{currentLng}_#{arg} in given object"

        new Handlebars.SafeString(val)

    Handlebars.registerHelper('trObj', trObj)
    trObj
