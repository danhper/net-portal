define [
    'handlebars'
    'jquery'
    'underscore'
    'flog'
    'cs!helpers/trObj'
], (Handlebars, $, _, flog, trObj) ->
    Handlebars.registerHelper 'classOrBlankTd', (dow, start_period, registrations) ->

        isInPeriod = (c) ->
            c.day_of_week == dow && c.start_period.id == start_period

        registration = _.find registrations, (r) ->
            _.find r.subject.classes, isInPeriod

        $content = $('<td>')

        if registration
            classObj = _.find registration.subject.classes, isInPeriod
            $content.append trObj(registration.subject, 'name').toString()
        else
            $content.append '&nbsp;'

        content = $('<div>').append($content).html()

        new Handlebars.SafeString(content)

