define [
    'handlebars'
], (Handlebars) ->
    zip = (lists...) ->
        listLengths = (li.length for li in lists)
        length = Math.min(listLengths...)
        for i in [0...length]
            li[i] for li in lists

    Handlebars.registerHelper('zip', zip)
    zip
