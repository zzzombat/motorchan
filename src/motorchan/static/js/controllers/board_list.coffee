class BoardListController
    constructor: ($scope, $log, BoardService) ->
        $scope.boards = BoardService.get()

angular.module('motorchan').controller 'BoardListController', ['$scope', '$log', 'BoardService', BoardListController]
