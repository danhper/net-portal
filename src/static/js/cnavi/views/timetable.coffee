define [
    'jquery'
    'underscore'
    'backbone'
    'flog'
    'cs!globalCollections/registration_list'
    'cs!globalCollections/period_list'
    'hbs!templates/cnavi/timetable'
], ($, _, Backbone, flog, registrationList, periodList, template) ->
    class TimetableView extends Backbone.View
        el: '#main'

        initialize: () ->
            @daysOfWeek = ["mon", "tue", "wed", "thu", "fri", "sat"]
            @collection = registrationList

        render: () ->
            flog.info "Rendering timetable"
            toShow = @collection.chain().filter((r) -> r.isAttending())
            @$el.html template({
                daysOfWeek: @daysOfWeek
                registrations: toShow.invoke('toJSON').value()
                periods: periodList.toJSON()
            })

    new TimetableView()
