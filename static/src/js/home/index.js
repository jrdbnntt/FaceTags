/**
 * /index
 *
 * Dynamically loads data into sample table
 */

(function() {
    'use strict';

    var API_URL = '/tags/get_user/';
    // API_URL = '/test/';

    var viewTable = $('table#view');
    var viewHeader = viewTable.find('thead tr');

    var columns = [
        { name: 'Tag', data: 'name', sWidth: '100px'},
        { name: 'Count', data: 'count', sWidth: '50px'},
        { name: 'Pictures', data: 'imgContainer'}
    ];

    getData()
    .then(parseData)
    .then(initializeTable)
    .fail(function(error) {
        console.error(error);
    });

    function getData() {
        var dfd = $.Deferred();
        $.ajax({
            method: 'GET',
            url: API_URL,
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
                [25, 50, 100, 200, -1],
                [25, 50, 100, 200, 'All']
            ],
            iDisplayLength: 25,
        });

        return $.when();
    }

})();
