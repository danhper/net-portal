define [
    'jquery'
    'underscore'
    'backbone'
    'flog'
    'cs!globalCollections/registration_list'
    'cs!views/includes/subject_row'
    'hbs!templates/cnavi/home/body'
], ($, _, Backbone, flog, registrationList, SubjectRow, template) ->
    class HomeView extends Backbone.View
        el: '#main'

        initialize: () ->
            @collection = registrationList
            @category = 'attending'

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

        removeOne: (view, force=false) ->
            if @category == 'favorite' or force
                view.remove()

        addAll: (category='attending') ->
            @$('tbody').empty()
            try
                toShow = _.chain @collection.filter((model) -> model.inCategory category)
                toShow.each((model) => @addOne model)
            catch error
                flog.warn error

        render: (category=@category) ->
            flog.info "Rendering category #{category}"
            @category = category
            @$el.html template()
            @$('.left-tools li').removeClass('active')
            @$(".#{category}").addClass('active')
            @addAll category
            this

    new HomeView()
