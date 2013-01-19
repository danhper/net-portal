define [
    'handlebars'
    'i18next',
    'cs!helpers/t'
], (Handlebars, i18next, t) ->
    classTime = (classObj) ->
        val = if classObj.day_of_week? then t "time.dow.#{classObj.day_of_week}" else t 'time.na'

        if classObj.start_period? and classObj.end_period?
            start = classObj.start_period.pk
            end = classObj.end_period.pk
            if start == end
                val += t("time.period", start)
            else
                val += t("time.period_interval", start, end)

        new Handlebars.SafeString(val)

    Handlebars.registerHelper('classTime', classTime)
    classTime
