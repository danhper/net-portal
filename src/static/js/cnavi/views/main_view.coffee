define [
    'jquery'
    'underscore'
    'backbone'
    'hbs!templates/test'
], ($, _, Backbone, template) ->
    class MainView extends Backbone.View
        el: 'body'

        initialize: () ->
            @$el.append template({foo: 'bar'})

    initialize: () ->
        new MainView()

