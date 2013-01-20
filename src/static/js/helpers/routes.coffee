define [
    'text!config/routes.json'
  , 'json2'
], (routes, JSON) ->
    JSON.parse routes
