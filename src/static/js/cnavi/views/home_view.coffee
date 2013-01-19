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


        addOne: (model) ->
            subject = new SubjectRow({ model: model })
            @$('tbody').append(subject.render().$el)


        render: () ->
            @$el.html template()
            @collection.each((model) => @addOne(model))
            this

    new HomeView()


