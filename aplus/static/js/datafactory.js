angular.module("aplusApp").service('dataFactory', ['$http', function ($http) {

  var urlBase = '/api';

  this.getScores = function (
    year, 
    school, 
    grade, 
    subject, 
    subset) {
  return $http.get(urlBase + '/' + year + '/' + school + '/' + grade 
      + '/' + subject + '/' + subset);
  };

  this.getSchoolOpt = function (first, second) {
    return $http.get(urlBase + '/school/option/1/'+ first + '/2/' + second);
  };

  this.getSchoolScores = function (
      year, 
      school, 
      grade, 
      subject, 
      subset) {
    return $http.get(urlBase + '/school/' + school + '/' + year + '/' + grade 
        + '/' + subject + '/' + subset);
  };
    }]);