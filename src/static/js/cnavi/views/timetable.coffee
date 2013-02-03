define [
    'jquery'
    'underscore'
    'backbone'
    'flog'
    'cs!globalCollections/registration_list'
    'cs!globalCollections/period_list'
    'hbs!templates/cnavi/timetable/timetable'
], ($, _, Backbone, flog, registrationList, periodList, template) ->
    class TimetableView extends Backbone.View
        el: '#main'

        initialize: () ->
            @daysOfWeek = ["mon", "tue", "wed", "thu", "fri", "sat"]
            @collection = registrationList

        render: () ->
            flog.info "Rendering timetable"
            toShow = @collection.chain().filter (r) -> r.isAttending()

            $html = $ template
                daysOfWeek: @daysOfWeek
                registrations: toShow.invoke('toJSON').value()
                periods: periodList.toJSON()

            @stripExtraTds $html

            @$el.html $('<div>').append($html).html()

        stripExtraTds: ($html) ->
            rowspanTds = $html.find('tbody tr td').filter (i) ->
                $(this).attr('rowspan') >= 2

            rowspanTds.each (id) ->
                $this = $(this)
                $tr = $this.parent 'tr'
                index = $tr.find('td').index($this)
                for _ in [2..$this.attr('rowspan')]
                    $tr = $tr.next()
                    $tr.find('td').eq(index).remove()

    new TimetableView()
