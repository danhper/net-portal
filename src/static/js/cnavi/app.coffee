define [
    'jquery'
    'underscore'
    'backbone'
    'i18next'
    'cs!views/main_view'
], ($, _, Backbone, i18next, MainView) ->
    i18nOptions =
        ns:
            namespaces: [
                'cnavi'
            ]
        defaultNs: 'cnavi'
        resGetPath: '/static/locales/__lng__/__ns__.json'
        lng: 'ja'  # need to change dynamically
    initialize: () ->
        i18next.init i18nOptions
        console.log i18next.t('foo')
        MainView.initialize()



