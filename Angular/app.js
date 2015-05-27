(function(){
  

  var app = angular.module('gemStore', []);



  app.controller('contr',function($scope,$http){

    $scope.events = [];
    $scope.appInfo = {};

  });


  app.controller('formController', function($scope,$http){
  	$scope.params = {};

  	$scope.refreshApp = function(params){
      
      $scope.events.splice(0);
      //160622

	  //host = `http://127.0.0.1/json1`
	  host = `http://ksenz-v:82/json`
	  
      //req = `http://127.0.0.1/json/applications?q={"filters":[{"name": "id", "op": "eq", "val": "${params.appId}"}]}`
      //req = `http://127.0.0.1/json1/Applications/${params.appId}`
	  req = host + `/Applications/${params.appId}`
      $http.get(req).success(function(data){
        appInfo = data;
        $scope.appInfo['id'] = appInfo.id;
        $scope.appInfo['base'] = appInfo.base;
    });
      
      //req = `http://127.0.0.1/json/events?q={"filters":[{"name": "applicationId", "op": "eq", "val": "${params.appId}"}]}`
      //req = `http://127.0.0.1/json1/Events/${params.appId}`
	  req = host + `/Events/${params.appId}`
      $http.get(req).success(function(data){
        
        //$scope.temp.text = ''
        events = data
        for (var i = 0; i< events.length; i++) {
          $scope.events.push(events[i]);
        };
        
    });


  	};

  });

})();
