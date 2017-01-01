'use strict';

var dim = dimensions(),
    width = dim.width,
    height = dim.height,
    modal_selector,
    h;

// Check location hash and load data accordingly, also set active data and color selects.
if (h = document.location.hash) {
    var c = h.replace('#', '');
    if (c == 'info' || c == 'table') {
        // Set this variable so modal can later be shown when DOM is ready.
        modal_selector = '#' + c + '-modal';
    } else if (-1 !== config.columns.indexOf(c)) {
        column = c;
    }
}

if (!column) {
    column = config.columns[0];
}

if (config.columns.length > 1) {
    document.querySelector('a[href="#' + column + '"]').parentNode.setAttribute('class', 'active');
}

$(function () {
    modal_selector && $(modal_selector).modal();
    $('#table').click(function () {
        var rows = d3.values(map.data),
            labels = d3.keys(rows[0]);

        var table = d3.select('#table-modal .table');

        var theader = table.append('thead').append('tr');
        theader.selectAll('th').data(labels).enter().append('th').text(function (d) {
            return d;
        });

        var tbody = table.append('tbody');
        var tr = tbody.selectAll('tr').data(rows).enter().append('tr').html(function (d) {
            return d3.values(d).map(function (e) {
                return '<td>' + e + '</td>';
            }).join('');
        });

        Sortable.init();
    });
});