$(document).ready(function() {
    // Initialize table
    var table = $('#recipe_table').DataTable({
        data : [],
        columns : [ {title : "Recipe"} ]
    });

    var ingredientByRecipeTable = $('#ingredient_table_by_recipe').DataTable({
        data : [],
        columns : [ {title : "Ingredient"} ]
    });

    var totalIngredientsTable = $('#ingredient_table').DataTable({
        data : [],
        columns : [ {title : "Ingredient"} ]
    });
    $(".recipe-search").keypress(function (e) {
        if (e.which == 13) {
            $.getJSON("/data/recipes/" + $(this).val(), function (recipes) {
                // Destroy table so we can reload data
                table.destroy();
                var data = [];
                $.each(recipes, function(key, row) {
                    data.push([row]);
                });
                table = $('#recipe_table').DataTable({
                    select: {
                        style: 'single'
                    },
                    data : data,
                    columns : [ {title : "Recipe"} ]
                });

                table.on('select', function ( e, dt, type, indexes ) {
                    var rowData = table.rows( indexes ).data().toArray();
                    //events.prepend( '<div><b>'+type+' selection</b> - '+JSON.stringify( rowData )+'</div>' );
                    console.log(rowData);
                    var recipeName = rowData[0];
                    console.log("hello");
                    $.getJSON("/data/recipe/ingredients/" + recipeName, function (ingredients) {
                        console.log(ingredients);
                        $(".total-ingredients").css("display", "none");
                        $(".ingredients-by-recipe").css("display", "block");
                        var data = [];
                        $.each(ingredients, function(key, row) {
                            data.push([row]);
                        });
                        ingredientByRecipeTable.destroy();

                        ingredientByRecipeTable = $('#ingredient_table_by_recipe').DataTable({
                            select: {
                                style: 'single'
                            },
                            data : data,
                            columns : [ {title : "Ingredient"} ]
                        });

                        ingredientByRecipeTable
                        .on( 'select', function ( e, dt, type, indexes ) {
                            var rowData = ingredientByRecipeTable.rows( indexes ).data().toArray();
                            //events.prepend( '<div><b>'+type+' selection</b> - '+JSON.stringify( rowData )+'</div>' );
                            var ingredient = rowData[0][0];
                            queryGwfAndUpdateBarChart(ingredient);
                            $(".chart-title.bar-title").text("Water Footprint for " + ingredient);
                            createMap(ingredient);
                        });

                        $.getJSON("/data/recipe/waterfootprint/" + ingredients.join(), function (footprint) {
                            console.log(footprint);
                            updateBarChartGWF(footprint);
                            $(".chart-title.bar-title").text("Average Water Footprint for all ingredients in " + recipeName);
                        });

                    });
                });
            });
        }
    });

	// Load ingredients
	$.getJSON('/data/ingredients', function(data_json) {
		console.log(data_json.slice(0,10));		
		var data = [];
		$.each(data_json, function(key, row) {
			data.push([row]);
		});
		console.log(data.slice(0,10));
		totalIngredientsTable.destroy();

		totalIngredientsTable = $('#ingredient_table').DataTable({
			select: {
	            style: 'single'
	        },
			data : data,
			columns : [ {title : "Ingredient"} ]
		});
		
		totalIngredientsTable
        .on( 'select', function ( e, dt, type, indexes ) {
            var rowData = totalIngredientsTable.rows( indexes ).data().toArray();
            //events.prepend( '<div><b>'+type+' selection</b> - '+JSON.stringify( rowData )+'</div>' );
            var ingredient = rowData[0][0];
            queryGwfAndUpdateBarChart(ingredient);
            createMap(ingredient);
        } );
		
	});

});
