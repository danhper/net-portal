define [
    'jquery'
    'underscore'
    'backbone'
    'cs!globalModels/subject'
    'cs!globalModels/term_period'
    'cs!helpers/getCookie'
], ($, _, Backbone, Subject, TermPeriod, getCookie) ->
    class SubjectRegistration extends Backbone.RelationalModel

        relations: [
            type: 'HasOne'
            key: 'subject'
            relatedModel: Subject
            reverseRelation:
                key: 'registrations'
                type: 'HasMany'
        ,
            type: 'HasOne'
            key: 'period'
            relatedModel: TermPeriod
        ]

        initialize: () ->

        isAttending: () ->
            today = new Date()
            @get('period').get('start_date') <= today && @get('period').get('end_date') >= today

        hasAttended: () ->
            today = new Date()
            @get('period').get('end_date') < today

        willAttend: () ->
            today = new Date()
            @get('period').get('start_date') > today

        save: (attributes, options) ->
            options ?= {}
            options.url = 'registration/update'
            options.type = 'POST'
            options.headers = { 'X-CSRFToken': getCookie('csrftoken')}
            super attributes, options

        inCategory: (category) ->
            switch category
                when 'attending' then @isAttending()
                when 'attended' then @hasAttended()
                when 'willAttend' then @willAttend()
                when 'favorite' then @get('favorite')
                else throw "Unknown category #{category}"


    SubjectRegistration.setup()
    SubjectRegistration
