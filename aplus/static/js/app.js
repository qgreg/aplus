'use strict';

/**
 * @ngdoc object
 * @name aplusApp
 * @requires ui.bootstrap
 *
 * @description
 * Root app, which routes and specifies the partial html and controller depending on the url requested.
 *
 */
var app = angular.module("aplusApp", ['chart.js', 'ngRoute', 'ui.bootstrap']);

app.config(['$interpolateProvider', function($interpolateProvider) {
      $interpolateProvider.startSymbol('{a');
      $interpolateProvider.endSymbol('a}');
    }]);

app.config(['$routeProvider',
        function ($routeProvider) {
            $routeProvider
                .when('/browser', {
                    templateUrl: '/static/partials/browser.html',
                    controller: 'BrowserCtrl'
                })
                .when('/compare', {
                    templateUrl: '/static/partials/donut.html',
                    controller: 'DoughnutCtrl'
                })
                .when('/', {
                    templateUrl: '/static/partials/home.html'
                })
                .otherwise({
                    redirectTo: '/'
                });
        }]);

app.controller('MainCtrl', ['$route',
  function MainCtrl($route) {
    this.$route = $route;
}]);

app.controller('DoughnutCtrl', ['$scope', 'dataFactory',
    function ($scope, dataFactory) {

    $scope.year = '2016';
    $scope.subject = 'ELA';
    $scope.school = 'PPS Phillips';
    $scope.grade = '3';
    $scope.subset = 'All';
    $scope.donutload = false;
    $scope.fullid = $scope.year + $scope.subject + $scope.school + $scope.grade + $scope.subset
    $scope.colors = ['#60B064', '#9DDBB5', '#D2A6D2', '#BA66B0'];
    $scope.options = {
        legend: {
            display: true,
            position: 'bottom'
    }};

    $scope.status;
    $scope.scores;
    $scope.labels;
    $scope.data;

    $scope.getScores = function () {
        dataFactory.getScores($scope.year, $scope.school, $scope.grade, $scope.subject, $scope.subset)
            .then(
                function (response) {
                    $scope.status = 'Retrieved score!';
                    $scope.scores = response.data;
                    $scope.labels = ['Advanced ' + ($scope.scores.advanced * 100).toFixed(1) + '%', 'Proficient '  + ($scope.scores.proficient * 100).toFixed(1) + '%', 'Basic ' + ($scope.scores.basic * 100).toFixed(1) + '%', 'Below Basic ' + ($scope.scores.below_basic * 100).toFixed(1) + '%'];
                    $scope.data = [$scope.scores.advanced, $scope.scores.proficient, $scope.scores.basic, $scope.scores.below_basic];
                    $scope.donutload = true;
                    // var myPie = new Chart(document.getElementById($scope.fullid).getContext("2d")).Doughnut($scope.data, $scope.labels, $scope.options);
                    var canvas = document.getElementById($scope.fullid);
                    var ctx = canvas.getContext("2d");
                    ctx.font = "10px Arial";
                    var topScore = (($scope.scores.advanced + $scope.scores.proficient) * 100).toFixed(1);
                    ctx.fillText("Hello",0,0);
                    ctx.fillText(topScore + "%",10,50);
                }, 
                function (error) {
                    $scope.status = 'Error retrieving score! ' + error.message;
                })
    };
}]);

