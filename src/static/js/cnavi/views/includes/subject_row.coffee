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
            'hover th': 'toggleDragIcon'
            'click .favorite-icon': 'toggleFavorite'

        toggleDragIcon: (e) ->
            $icon = @$(e.target).find('.drag-icon')
            $icon.css 'visibility', if e.type == 'mouseenter' then 'visible' else 'hidden'

        toggleFavorite: (e) ->
            flog.info 'Favorite button clicked'
            if @model.get('favorite') == $(e.target).hasClass('icons-favorite_on')
                @model.set('favorite', not @model.get('favorite'))
                @model.save()
            @render()

        render: () ->
            @$el.html template({ registration: @model.toJSON() })
            this

    SubjectRow
