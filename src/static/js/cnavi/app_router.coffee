define [
    'jquery'
    'underscore'
    'backbone'
    'cs!views/home_view'
], ($, _, Backbone, homeView) ->
    class AppRouter extends Backbone.Router

        initialize: () ->

        routes:
            '*path': 'home'

        home: () ->
            homeView.render()


    initialize: () ->
        new AppRouter()
        Backbone.history.start()
