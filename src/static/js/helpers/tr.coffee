define [
    'handlebars'
  , 'i18next'
  , 'cs!helpers/t'
], (Handlebars, i18next, t) ->
    tr = (namespace, keys, key, args...) ->
        key = "#{namespace}:#{keys}.#{key}"
        t key

    Handlebars.registerHelper('tr', tr)
    tr
