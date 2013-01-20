define [
    'handlebars'
  , 'i18next'
], (Handlebars, i18next) ->
    t = (key, args...) ->
        val = i18next.t(key)

        # replace variables in apparition order
        while res = /__.*?__/.exec(val)
            val = val.replace(res, args.shift())

        new Handlebars.SafeString(val)

    Handlebars.registerHelper('t', t)
    t
