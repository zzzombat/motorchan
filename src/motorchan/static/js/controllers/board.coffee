class BoardController
    constructor: ($scope, $routeParams, $log, BoardService, ThreadService) ->
        $scope.threads = ThreadService.get
            board: $routeParams.board
            page: $routeParams.page or 1
        $scope.board = BoardService.get
            slug: $routeParams.board

angular.module('motorchan').controller 'BoardController', ['$scope', '$routeParams', '$log', 'BoardService', 'ThreadService', BoardController]
