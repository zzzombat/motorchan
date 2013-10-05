class Routes
    constructor: ($routeProvider) ->
        $routeProvider
        .when '/',
            controller: 'BoardListController'
            templateUrl: '/static/templates/boards.html'
        .otherwise
            redirectTo: '/'

angular.module('motorchan').config ['$routeProvider', Routes]
