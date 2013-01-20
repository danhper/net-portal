define [
    'jquery'
    'underscore'
    'backbone'
    'hbs!templates/cnavi/home/subject'
], ($, _, Backbone, template) ->
    class SubjectRow extends Backbone.View
        tagName: 'tr'

        initialize: () ->

        render: () ->
            @$el.html template({ registration: @model.toJSON() })
            this

    SubjectRow
