define [
    'jquery'
    'underscore'
    'backbone'
    'hbs!templates/cnavi/header'
], ($, _, Backbone, template) ->
    class HeaderView extends Backbone.View
        el: '#header'

        initialize: () ->
            context = { user: { jp_first_name: 'ダニエル' }}
            @$el.html template(context)

    HeaderView
