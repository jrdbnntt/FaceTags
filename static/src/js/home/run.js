/**
 * /run
 *
 * Dynamically loads data into sample table
 */

/* globals FB */
(function() {
    'use strict';

    var API_URL = '/tags/get_user/';
    var token = null;
    var view = $('#view');
    var viewTable = view.find('table');
    var viewHeader = viewTable.find('thead tr');
    var viewLoading = view.find('.loading-message');
    var fbLog = view.find('fb.loading-message');
    var loadInterval;

    var columns = [
        { name: 'Tag', data: 'name', sWidth: '100px'},
        { name: 'Count', data: 'count', sWidth: '50px'},
        { name: 'Pictures', data: 'imgContainer'}
    ];

    function startLoading() {
        viewLoading.text('Loading ');
        var elipContainer = $('span').appendTo(viewLoading);
        viewLoading.show();

        elipContainer.empty();
        loadInterval = setInterval(function() {
            if (elipContainer.text().length < 6) {
                elipContainer.text(elipContainer.text() + '. ');
            } else {
                elipContainer.empty();
            }
        }, 500);

        return $.when();
    }

    function stopLoading() {
        clearInterval(loadInterval);
        viewLoading.hide();
        return $.when();
    }

    function getData() {
        var dfd = $.Deferred();
        $.ajax({
            method: 'GET',
            url: API_URL,
            data: {
                'token': token
            },
            success: function(res) {
                if (res.error) {
                    console.error(res);
                    dfd.reject(res.error);
                }
                if (!res.data) {
                    console.error(res);
                    dfd.reject('No data returned');
                }

                dfd.resolve(res.data);
            },
            error: function(error) {
                dfd.reject(error);
            }
        });
        return dfd.promise();
    }


    /**
     * Grabs column data from rows
     */
    function parseData(rows) {
        var dfd = $.Deferred();
        var imgUrls = 'image_urls';

        if (rows.length > 0) {

            // Convert image urls to img tags
            $.each(rows, function(i, row) {
                row.imgContainer = '<div class="pic-container">';

                row[imgUrls].forEach(function(url) {
                    row.imgContainer += '<a target="_blank" href="'+url+'"><img class="img-responsive" src="'+url+'"/></a>';
                });

                row.imgContainer += '</div>';
            });
        }

        return dfd.resolve({
            cols: columns,
            rows: rows
        });
    }

    function initializeTable(tableData) {
        tableData.cols.forEach(function(col) {
            viewHeader.append('<th>'+col.name+'</th>');
        });

        viewTable.DataTable({
            data: tableData.rows,
            // scrollX: true,
            columns: tableData.cols,
            order: [[1, 'desc']],
            aLengthMenu: [
                [5, 10, 15, 20, -1],
                [5, 10, 15, 20, 'All']
            ],
            iDisplayLength: 25,
        });

        return $.when();
    }

    // Facebook Stuff
    window.checkLoginState = function() {
        FB.getLoginStatus(function(response) {
            statusChangeCallback(response);
        });
    };

    function statusChangeCallback(response) {
        console.log(response);
        if (response.status === 'connected') {
            fbLog.hide();
            token = response.authResponse.accessToken;

            startLoading()
            .then(getData)
            .then(parseData)
            .then(initializeTable)
            .then(stopLoading)
            .fail(function(error) {
                console.error(error);
                stopLoading();
                viewLoading.text('Error!');
            });
        } else {
            alert('There was an error connecting to Facebook');
            viewLoading.text('Error!');
        }
    }

    window.fbAsyncInit = function() {
        FB.init({
            appId      : '1074510792606997',
            xfbml      : true,
            version    : 'v2.6'
        });

        FB.getLoginStatus(function(response) {
            statusChangeCallback(response);
        });
    };

    (function(d, s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "//connect.facebook.net/en_US/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

})();