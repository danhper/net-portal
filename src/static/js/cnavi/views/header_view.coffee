define [
    'jquery'
    'underscore'
    'backboneAll'
    'hbs!templates/cnavi/header'
    'cs!common/current_user'
], ($, _, Backbone, template, currentUser) ->
    class HeaderView extends Backbone.View
        el: '#header'

        initialize: () ->
            context = { user: { jp_first_name: 'ダニエル' }}
            @$el.html template(context)

    HeaderView
