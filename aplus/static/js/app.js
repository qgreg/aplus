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
var app = angular.module(
    "aplusApp", ['chart.js', 'ngRoute', 'ui.bootstrap', 'ngTable']);

app.config(['$interpolateProvider', function($interpolateProvider) {
      $interpolateProvider.startSymbol('{a');
      $interpolateProvider.endSymbol('a}');
    }]);

app.config(["$routeProvider","$locationProvider", function (
    $routeProvider,$locationProvider) {
  $routeProvider
    .when('/browse', {
        templateUrl: '../static/partials/select.html',
        controller: 'BrowserCtrl'
    })
    .when('/compare', {
        templateUrl: '../static/partials/compare.html',
        controller: 'CompareCtrl'
    })
    .when('/list', {
        templateUrl: '../static/partials/listschool.html',
        controller: 'ListCtrl'
    })
    .when('/', {
        templateUrl: '../static/partials/home.html'
    })
    .otherwise({
        redirectTo: '/'
    });
  $locationProvider.hashPrefix('');
}]);


app.controller('MainCtrl', ['$route',
  function MainCtrl($route) {
    this.$route = $route;
}]);


app.controller('BrowserCtrl', ['$scope', '$http', 'ngResource', 'dataFactory',
    function ($scope, $http, ngResource, dataFactory) {

    $scope.pssa = {
    "year": "",
    "subject": "",
    "school": "",
    "grade": "",
    "subset": ""
    };

    $http.get('/api/pssa/select')
        .then(function (result) {
            $scope.select = result.data;
        });

    $scope.status;

    $scope.getScores = function () {
      dataFactory.getScores($scope.pssa.year, $scope.pssa.school, 
          $scope.pssa.grade, $scope.pssa.subject, $scope.pssa.subset)
        .then(
          function (response) {
            $scope.status = 'Retrieved score!';
            $scope.score = response.data;
            if ($scope.score.hasOwnProperty('total_tested')) {
              $scope.score.labels = [
                  'Advanced ' + $scope.score.advanced + ' ' + (
                      $scope.score.advanced / $scope.score.total_tested 
                      * 100).toFixed(1) + '%', 
                  'Proficient ' + $scope.score.proficient + ' ' + (
                      $scope.score.proficient / $scope.score.total_tested 
                      * 100).toFixed(1) + '%', 
                  'Basic ' + $scope.score.basic + ' ' + (
                      $scope.score.basic / $scope.score.total_tested 
                      * 100).toFixed(1) + '%', 
                  'Below Basic ' + $scope.score.below_basic + ' ' + (
                      $scope.score.below_basic / $scope.score.total_tested 
                      * 100).toFixed(1) + '%'];
              $scope.score.data = [
                  $scope.score.advanced, 
                  $scope.score.proficient, 
                  $scope.score.basic, 
                  $scope.score.below_basic];
            };
          $scope.score.fullid = $scope.score.year + $scope.score.subject 
              + $scope.score.school + $scope.score.grade + $scope.score.subset
          $scope.colors = ['#60B064', '#9DDBB5', '#D2A6D2', '#BA66B0'];
          $scope.options = {
              legend: {
                  display: true,
                  position: 'bottom'
               }};
          }, 
          function (error) {
            $scope.status = 'Error retrieving score! ' + error.message;
          })
    };

}]);


app.controller('ListCtrl', ['$scope', '$http', function ($scope, $http) {

    $scope.entryView = {"status": true};

    $scope.schoolTypeOpt = {
    "Elementary": "Elementary",
    "Middle": "Middle",
    "High": "High"
    };

    $scope.pssa = {
    "year": "",
    "subject": "",
    "school": "",
    "grade": "",
    "subset": ""
    };

    $scope.status;
    $scope.scores = {"data": ""};

    $scope.getSchoolList = function () {
      $http.get('/api/pssa/list/' + $scope.schoolType)
        .then(function (result) {
          $scope.select = result.data;
        })
    };

}]);


app.controller('ListTableCtrl', [
    '$scope', '$route', 'dataFactory', 'NgTableParams', 
        function ($scope, $route, dataFactory, NgTableParams) {

    var tabParams = {
        page: 1,            // show first page
        count: 10,          // count per page
        sorting: { school: "asc" }
    };
    var theData = []

    $scope.getListScores = function () {
        dataFactory.getListScores(
            $scope.pssa.year,
            $scope.pssa.grade,
            $scope.pssa.subject,
            $scope.pssa.subset)
          .then(
            function (response) {
                $scope.status = 'Retrieved score!';
                $scope.scores = response.data;
                var theData = angular.copy($scope.scores['data']);
                $scope.tableParams = new NgTableParams(
                    tabParams, {dataset: theData});
                $scope.entryView.status = false;
            }
          )
      };

$scope.reloadRoute = function() {
   $route.reload();
};

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

app.controller('CompareCtrl', ['$scope', '$http', 'dataFactory',
    function ($scope, $http, dataFactory) {

    $scope.schoolTypeOpt = {
    "Elementary": "Elementary",
    "Middle": "Middle",
    "High": "High"
    };

    $scope.schools = {
    "first": "",
    "second": "",
    };

    $scope.pssa = {
    "year": "",
    "subject": "",
    "grade": "",
    "subset": "",
    "ready": false
    };

    $scope.schoolType = "";
    $scope.schoolList = "";
    $scope.schoolOpt = "";

    $scope.getSchoolList = function () {
        $http.get('/api/school/type/' + $scope.schoolType)
        .then(function (result) {
            $scope.schoolList = result.data;
        })};

    $scope.getSchoolOpt = function (first, second) {
        dataFactory.getSchoolOpt(first, second)
        .then(function (result) {
            $scope.schoolOpt = result.data;
        })};

    $scope.getSchoolScores = function (school, pssa, num) {
        dataFactory.getSchoolScores(pssa.year, school, pssa.grade, pssa.subject, pssa.subset)
            .then(
                function (response) {
                    $scope.status = 'Retrieved score!';
                    $scope['scores' + num] = response.data;
                }, 
                function (error) {
                    $scope.status = 'Error retrieving score! ' 
                        + error.message;
                })};

    $scope.getChartParam = function (score) {
      if (score.hasOwnProperty('total_tested')) {
        score.labels = [
            'Advanced ' + score.advanced + ' ' + (
                    score.advanced / score.total_tested * 100
                ).toFixed(1) + '%',
            'Proficient ' + score.proficient + ' ' + (
                score.proficient / score.total_tested * 100
                ).toFixed(1) + '%',
            'Basic ' + score.basic + ' ' + (
                score.basic / score.total_tested * 100
                ).toFixed(1) + '%',
            'Below Basic ' + score.below_basic + ' ' + (
                score.below_basic / score.total_tested * 100
                ).toFixed(1) + '%'];
        };
      score.data = [
          score.advanced, score.proficient, score.basic, score.below_basic];
      score.fullid = score.year + score.subject + score.school + score.grade 
          + score.subset
      $scope.colors = ['#60B064', '#9DDBB5', '#D2A6D2', '#BA66B0'];
      $scope.options = {
            legend: {
                display: true,
                position: 'bottom'
            }};
      };
}]);


