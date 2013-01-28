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
            console.log @collection.toJSON()

        addOne: (model) ->
            subject = new SubjectRow({ model: model })
            @$('tbody').append(subject.render().$el)

        addAll: (category='attending') ->
            @$('tbody').empty()
            @collection.each((model) => @addOne(model))

        render: (category='attending') ->
            @$el.html template()
            @addAll(category)
            this

    new HomeView()


