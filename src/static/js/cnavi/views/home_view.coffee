define [
    'jquery'
    'underscore'
    'backbone'
    'cs!globalCollections/registration_list'
    'cs!views/includes/subject_row'
    'hbs!templates/cnavi/home/body'
], ($, _, Backbone, registrationList, SubjectRow, template) ->
    class HomeView extends Backbone.View
        el: '#main'

        initialize: () ->
            @collection = registrationList

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
            e.preventDefault()
            e.stopPropagation()
            $target = $(e.target)

        addOne: (model) ->
            subject = new SubjectRow({ model: model })
            @$('tbody').append subject.render().$el

        addAll: (category='attending') ->
            @$('tbody').empty()
            toShow = _.chain(@collection.filter((model) -> model.inCategory(category)))
            toShow.each((model) => @addOne model)

        render: (category='attending') ->
            @$el.html template()
            @$('.left-tools li').removeClass('active')
            @$(".#{category}").addClass('active')
            @addAll category
            this

    new HomeView()
