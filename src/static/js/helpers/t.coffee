define [
    'handlebars'
  , 'i18next'
], (Handlebars, i18next) ->
    t = (key, args...) ->
        val = i18next.t(key)
        vars = /__.*?__/.exec(val)

        # replace variables in apparition order
        if vars
            for arg, i in args
                if i < vars.length
                    val = val.replace(vars[i], arg)

        new Handlebars.SafeString(val)

    Handlebars.registerHelper('t', t)
    t
