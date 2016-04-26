/**
 * /index
 *
 * Dynamically loads data into sample table
 */

/* globals FB */
(function() {
    'use strict';

    var API_URL = '/tags/all/';
    var view = $('#view');
    var viewTable = view.find('table');
    var viewHeader = viewTable.find('thead tr');
    var viewLoading = view.find('.loading-message');
    var loadInterval;

    var columns = [
        { name: 'Tag', data: 'name', sWidth: '100px'},
        { name: 'Count', data: 'count', sWidth: '50px'}
    ];



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

    function startLoading() {
        viewLoading.text('Loading ');
        var elipContainer = $('<span></span>').appendTo(viewLoading);
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

})();
