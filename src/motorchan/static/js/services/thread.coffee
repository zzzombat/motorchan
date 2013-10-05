class ThreadService
    constructor: ($resource) ->
        Board = $resource '/static/stub/threads.json', {},
            query:
                method: 'GET'
                isArray: false

        ThreadService::get = (params) ->
            Board.query(params).$promise

angular.module('motorchan').service 'ThreadService', ['$resource', ThreadService]
