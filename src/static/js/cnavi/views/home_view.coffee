define [
    'jquery'
    'underscore'
    'backbone'
    'flog'
    'cs!globalCollections/registration_list'
    'cs!views/includes/subject_row'
    'hbs!templates/cnavi/home/body'
    'jqueryui/sortable'
], ($, _, Backbone, flog, registrationList, SubjectRow, template) ->
    class HomeView extends Backbone.View
        el: '#main'

        initialize: () ->
            @collection = registrationList
            @category = 'attending'
            @subjectViews = []

        events:
            'click .left-tools .search': 'search'
            'click .left-tools li:not(.search)': 'showCategory'

        showCategory: (e) ->
            $target = $(e.target)
            if $target.is 'a'
                $target.blur()
            else
                window.location.hash = $target.children('a').attr 'href'

        search: (e) ->
            flog.info 'Entered search function'
            e.preventDefault()
            e.stopPropagation()
            $target = $(e.target)

        addOne: (model) ->
            subject = new SubjectRow({ model: model })
            model.on 'change:favorite', (model) =>
                if not model.get 'favorite'
                    @removeOne subject
            @$('tbody').append subject.render().$el
            @subjectViews.push subject

        removeOne: (view, force=false) ->
            if @category == 'favorite' or force
                view.remove()

        addAll: (category='attending') ->
            @$('tbody').empty()
            @subjectViews = []
            try
                toShow = _.chain @collection.filter((model) -> model.inCategory category)
                toShow.each((model) => @addOne model)
            catch error
                flog.warn error

        makeSortable: () ->
            @$('tbody').sortable(
                containment: @$('tbody')
                handle: '.drag-icon'
                start: (e, ui) => ui.item.oldIndex = ui.item.index()
                stop: (e, ui) => @drop e, ui
            )

        drop: (e, ui) ->
            newPos = @subjectViews[ui.item.index()].model.get 'order'
            model = @subjectViews[ui.item.oldIndex].model

            model.set 'order', newPos
            # model.save()
            @reorderViewsList ui.item.oldIndex, ui.item.index()


        reorderViewsList: (oldIndex, newIndex) ->
            moved = @subjectViews[oldIndex]
            @subjectViews[oldIndex..oldIndex] = []
            @subjectViews[newIndex..newIndex] = [moved, @subjectViews[newIndex]]

        setActiveTab: (category) ->
            @$('.left-tools li').removeClass('active')
            @$(".#{category}").addClass('active')

        render: (category=@category) ->
            flog.info "Rendering category #{category}"
            @category = category
            @$el.html template()
            @setActiveTab category
            @addAll category
            @makeSortable()
            this

    new HomeView()
