define [
    'jquery'
    'underscore'
    'backboneAll'
    'hbs!templates/cnavi/header'
    'cs!common/current_user'
], ($, _, Backbone, template, currentUser) ->
    class HeaderView extends Backbone.View
        el: '#header'

        render: () ->
            context = { user: currentUser.toJSON() }
            @$el.html template(context)
            this

    new HeaderView()
