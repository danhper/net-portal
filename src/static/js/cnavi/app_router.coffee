define [
    'jquery'
    'underscore'
    'backbone'
    'cs!views/home_view'
], ($, _, Backbone, homeView) ->
    class AppRouter extends Backbone.Router

        initialize: () ->

        routes:
            'classes/:category': 'classes'
            '*path': 'classes'

        classes: (category='attending') ->
            homeView.render(if category then category else 'attending')


    initialize: () ->
        new AppRouter()
        Backbone.history.start()
