define [
    'handlebars'
    'i18next'
], (Handlebars, i18next) ->
    tr_o = (object, arg) ->
        currentLng = i18next.lng()




        new Handlebars.SafeString(val)

    Handlebars.registerHelper('tr_o', tr_o)
    t
