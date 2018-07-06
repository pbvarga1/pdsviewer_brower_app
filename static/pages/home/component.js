angular.module('homeApp').component('home', {
    templateUrl: '/static/pages/home/template.html',
    controller: function homeController($timeout, homeService) {
        $ctrl = this;
        $ctrl.style = {'-webkit-transform': 'rotate(0deg) scaleX(1) scaleY(1)'};
        $ctrl.rotate = 0;
        $ctrl.progress = 0;
        $ctrl.showProgress = false;
        $ctrl.flipY = 1;
        $ctrl.flipX = 1;
        $ctrl.imageUrl = '';
        $ctrl.imageSrc = '';
        $ctrl.errored = false;

        function getProgress() {
            homeService.getProgress().then(function(data) {
                $ctrl.progress = data.data.progress;
                if ($ctrl.progress < 100) {
                    $timeout(getProgress, 2000);
                } else {
                    $ctrl.showProgress = false;
                    $ctrl.progress = 0;
                    $ctrl.imageSrc = '/_get_image?url=' + $ctrl.imageUrl;
                }
            });
        }

        $ctrl.getImage = function() {
            $ctrl.errored = false;
            $ctrl.progress = 1;
            $ctrl.showProgress = true;
            $ctrl.imageSrc = '';
            homeService.cacheImage($ctrl.imageUrl).then(function(data) {
                getProgress();
            });
        };

        function handleImageError() {
            $ctrl.errored = true;
            $ctrl.imageSrc = '';
        }

        $ctrl.imageError = function() {
            $timeout(handleImageError(), 100);
            
            console.log('ERROR');
        }

        $ctrl.rotateImage = function() {
            if ($ctrl.rotate == 270) { 
                $ctrl.rotate = 0;
            } else {
                $ctrl.rotate += 90;
            }
            $ctrl.styleImage()
        }

        $ctrl.flipYImage = function() { 
            $ctrl.flipY *= -1;
            $ctrl.styleImage()
        }

        $ctrl.flipXImage = function() { 
            $ctrl.flipX *= -1;
            $ctrl.styleImage()
        }

        $ctrl.styleImage = function() {
            var style = 'rotate(Rdeg) scaleX(x) scaleY(y)';
            style = style.replace('R', $ctrl.rotate);
            style = style.replace('x', $ctrl.flipX);
            style = style.replace('y', $ctrl.flipY);
            $ctrl.style = {'-webkit-transform': style};
        }
    }
});