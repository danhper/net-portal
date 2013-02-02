define [
    'jquery'
    'underscore'
    'backbone'
    'flog'
    'hbs!templates/cnavi/home/subject'
], ($, _, Backbone, flog, template) ->
    class SubjectRow extends Backbone.View
        tagName: 'tr'

        initialize: () ->

        events:
            'click .favorite-icon': 'toggleFavorite'

        toggleFavorite: (e) ->
            flog.info 'Favorite button clicked'
            if @model.get('favorite') == $(e.target).hasClass('icons-favorite_on')
                @model.set('favorite', not @model.get('favorite'))
                @model.save()
            @render()

        render: () ->
            @$el.html template({ registration: @model.toJSON() })
            @$('th').hover(
                () => @$('.drag-icon').css('visibility', 'visible'),
                () => @$('.drag-icon').css('visibility', 'hidden')
            )
            this

    SubjectRow
