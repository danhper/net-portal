define [
    'cs!views/main_view'
    'i18next'
    'text'
], (MainView, i18next, text) ->
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
