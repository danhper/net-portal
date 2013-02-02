define [
    'jquery'
    'underscore'
    'backbone'
    'cs!views/sidebar_view'
    'cs!views/home_view'
    'cs!views/timetable'
], ($, _, Backbone, sidebarView, homeView, timetableView) ->
    class AppRouter extends Backbone.Router

        initialize: () ->

        routes:
            'classes/:category': 'classes'
            'timetable': 'timetable'
            '*path': 'classes'

        classes: (category='attending') ->
            sidebarView.changeActive 0
            homeView.render(if category then category else 'attending')

        timetable: () ->
            sidebarView.changeActive 1
            timetableView.render()

    initialize: () ->
        new AppRouter()
        Backbone.history.start()
