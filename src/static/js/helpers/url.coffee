define [
    'handlebars'
  , 'cs!helpers/routes'
  , 'cs!helpers/zip'
], (Handlebars, routes, zip) ->
    url = (routeKey, params) ->
        params ?= {}

        keys = routeKey.split(":")

        for key in keys
            if (route? and not route[key]) or (not route? and not routes[key])
                throw "No route for #{routeKey}."
            route = if route? then route[key] else routes[key]


        paramNames = /(:[a-zA-Z]+)/.exec(route)

        if paramNames
            for name in paramNames
                val = params[name]
                if not val
                    throw "Need param #{name} for route #{routeKey}"
                route = route.replace(name, val)

        new Handlebars.SafeString(route)

    Handlebars.registerHelper('url', url)
    url
