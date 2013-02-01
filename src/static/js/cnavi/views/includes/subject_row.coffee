define [
    'jquery'
    'underscore'
    'backbone'
    'hbs!templates/cnavi/home/subject'
], ($, _, Backbone, template) ->
    class SubjectRow extends Backbone.View
        tagName: 'tr'

        initialize: () ->

        events:
            'hover th': 'toggleDragIcon'
            'click .favorite-icon': 'toggleFavorite'

        toggleDragIcon: (e) ->
            $icon = @$(e.target).find('.drag-icon')
            $icon.css 'visibility', if e.type == 'mouseenter' then 'visible' else 'hidden'

        toggleFavorite: (e) ->
            if @model.get('favorite') == $(e.target).hasClass('icons-favorite_on')
                @model.set('favorite', not @model.get('favorite'))
                @model.save()
            @render()

        render: () ->
            @$el.html template({ registration: @model.toJSON() })
            this

    SubjectRow
