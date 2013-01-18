define 'app', (require) ->
    i18next = require 'i18next'
    MainView = require 'cs!views/main_view'
    text = require 'text'

    i18nOptions =
        ns:
            namespaces: [
                'cnavi'
            ]
            defaultNs: 'cnavi'
        debug: true
        resStore:
            ja: {}

    initialize: (lng='ja') ->
        moduleName = "text!locales/#{lng}/cnavi.json"
        require [moduleName], (t) ->
            translations = JSON.parse t

            i18nOptions.lng = lng
            i18nOptions.resStore[lng].cnavi = translations
            i18next.init i18nOptions

            MainView.initialize()



