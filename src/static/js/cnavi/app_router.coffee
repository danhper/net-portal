define [
    'jquery'
    'underscore'
    'backbone'
    'cs!views/home_view'
    'cs!views/timetable'
], ($, _, Backbone, homeView, timetableView) ->
    class AppRouter extends Backbone.Router

        initialize: () ->

        routes:
            'classes/:category': 'classes'
            'timetable': 'timetable'
            '*path': 'classes'

        classes: (category='attending') ->
            homeView.render(if category then category else 'attending')

        timetable: () ->
            timetableView.render()

    initialize: () ->
        new AppRouter()
        Backbone.history.start()
