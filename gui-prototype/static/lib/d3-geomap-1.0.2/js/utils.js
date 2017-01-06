'use strict';

var width, height, footer_width;

function getSVG(selector) {
    var whRatio = arguments[1] === undefined ? 1 : arguments[1];

    var sel = d3.select(selector);
    var bbox = sel.node().parentElement.getBoundingClientRect();
    return sel.attr('width', bbox.width).attr('height', bbox.width / whRatio);
}

function dimensions() {
    var min_width = 400,
        max_width = 1766,
        comp_width = d3.select('#map').node().getBoundingClientRect().width;
    if (comp_width > max_width) comp_width = max_width;
    if (comp_width < min_width) comp_width = min_width;

    footer_width = comp_width - 160, width = +comp_width;
    height = comp_width * 0.5;

    return { width: width, height: height };
}

// http://bl.ocks.org/larskotthoff/11406992
function arrangelabels(svg, selector) {
    var move = 1,
        distfactor = 2.7;

    while (move > 0) {
        move = 0;
        svg.selectAll(selector).each(function () {
            var that = this,
                a = this.getBoundingClientRect();
            svg.selectAll(selector).each(function () {
                if (this != that) {
                    var b = this.getBoundingClientRect();
                    if (Math.abs(a.left - b.left) * distfactor < a.width + b.width && Math.abs(a.top - b.top) * distfactor < a.height + b.height) {
                        // overlap, move labels
                        var dx = (Math.max(0, a.right - b.left) + Math.min(0, a.left - b.right)) * 0.01,
                            dy = (Math.max(0, a.bottom - b.top) + Math.min(0, a.top - b.bottom)) * 0.02,
                            tt = d3.transform(d3.select(this).attr('transform')),
                            to = d3.transform(d3.select(that).attr('transform'));
                        move += Math.abs(dx) + Math.abs(dy);

                        to.translate = [to.translate[0] + dx, to.translate[1] + dy];
                        tt.translate = [tt.translate[0] - dx, tt.translate[1] - dy];
                        d3.select(this).attr('transform', 'translate(' + tt.translate + ')');
                        d3.select(that).attr('transform', 'translate(' + to.translate + ')');
                        a = this.getBoundingClientRect();
                    }
                }
            });
        });
    }
}

// http://bl.ocks.org/mbostock/7555321
function wrap(text, width) {
    text.each(function () {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.1,
            // ems
        y = text.attr('y'),
            dy = parseFloat(text.attr('dy')),
            tspan = text.text(null).append('tspan').attr('x', 0).attr('y', y).attr('dy', dy + 'em');
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(' '));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                tspan.text(line.join(' '));
                line = [word];
                tspan = text.append('tspan').attr('x', 0).attr('y', y).attr('dy', ++lineNumber * lineHeight + dy + 'em').text(word);
            }
        }
    });
}

function sluggify(s) {
    return s.toLowerCase().replace(/[^\w -]+/g, '').replace(/ +/g, '-');
}

function title(map) {
    document.title = config.title;
    if (config.hasOwnProperty('columns') && config.columns.length > 1 && map.hasOwnProperty('column')) {
        document.title += ': ' + map.column();
    }
    return document.title;
}

function annotation(map) {
    var rh = 75,
        svg = map.svg,
        xOffset = 160;

    svg.select('g.footer').remove();

    var fg = svg.append('g').attr('class', 'footer').attr('width', '100%').attr('height', rh).attr('transform', 'translate(0,' + (height - rh) + ')');

    fg.append('rect').attr('class', 'footer').attr('width', footer_width).attr('height', rh).attr('x', xOffset);

    fg.append('text').attr('class', 'title').attr('width', footer_width).attr('x', xOffset).attr('y', 20).text(title(map));

    fg.append('text').attr('width', footer_width).attr('x', xOffset).attr('y', 35).text('Data: ');

    fg.append('svg:a').attr('xlink:href', config.data[0].source).append('svg:text').text(config.data[0].source.replace('http://', '')).attr('class', 'link').attr('x', xOffset + 32).attr('y', 35);

    fg.append('text').attr('width', footer_width).attr('x', xOffset).attr('y', 50).text('Source: ');

    fg.append('svg:a').attr('xlink:href', config.canonical).attr('class', 'map_source').append('svg:text').text(config.canonical.replace('http://', '')).attr('class', 'link').attr('x', xOffset + 44).attr('y', 50);

    fg.append('text').attr('x', xOffset).attr('y', 65).text('CC BY-SA 2014 Ramiro Gómez');
}