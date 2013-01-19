define [
    'jquery'
    'underscore'
    'backbone'
    'hbs!templates/cnavi/home/subject'
], ($, _, Backbone, template) ->
    class HomeView extends Backbone.View
        tagName: 'tr'

        initialize: () ->


        render: () ->
            @$el.html template({ registration: @model.toJSON() })
            this

    HomeView


