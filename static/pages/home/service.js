angular.module('homeApp').service('homeService', function($http) {
    this.getProgress = function() { 
        return $http.get('/_get_progress');
    }
    this.cacheImage = function(url) {
        return $http.post('/_cache_image', data={url: url});
    }
});