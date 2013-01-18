define [
    'jquery'
    'underscore'
    'backbone'
], ($, _, Backbone) ->
    class AppView extends Backbone.View
        el: 'body'

        initialize: () ->
            @$el.append(@template({foo: 'bar'}))

    return {
        initialize: () ->
            new AppView
    }
