define [
    'jquery'
    'underscore'
    'backbone'
    'cs!views/header_view'
], ($, _, Backbone, HeaderView) ->
    class MainView extends Backbone.View
        el: 'body'

        initialize: () ->
            new HeaderView()

    initialize: () ->
        new MainView()

