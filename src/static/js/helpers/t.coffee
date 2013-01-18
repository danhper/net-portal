define [
    'handlebars'
  , 'i18next'
], (Handlebars, i18next) ->
    t = (key, context) ->
        context ?= {}
        console.log i18next.t(key, context)
        i18next.t(key, context)

    Handlebars.registerHelper('t', t)
    t
