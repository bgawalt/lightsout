$(document).ready(function() {
    var lights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    var game_won = false;
    var counter = 0;
    var explainer_shade = 200;

    // TODO: Swap "active" and "inactive" nomenclature.
    var active_bg = '#411111';
    var active_fg = '#553300';
    var inactive_bg = '#EEBB22';
    var inactive_fg = '#DDDD33';

    var prettyPrintCounter = function() {
        return counter.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",").concat(" moves");
    }

    var set_colors = function() {
        $("#count").html(prettyPrintCounter)
        for (a = 0; a < lights.length; a++) {
            col = a % 4;
            row = (a - col) / 4;
            cell = "#"+row.toString()+col.toString();
            if (lights[a] === 0) {
                $(cell).css('background-color', inactive_bg)
                $(cell).css('color', inactive_fg)
            }
            else {
                $(cell).css('background-color', active_bg)
                $(cell).css('color', active_fg)
            }
        }
    }

    var toggle = function(row, col) {
        if (row >= 0 && row < 4 && col >= 0 && col < 4) {
            var idx = 4*row + col;
            lights[idx] = 1 - lights[idx];
        }
    }
    
    var toggle_neighbors = function(row, col) {
        toggle(row + 1, col);
        toggle(row - 1, col);
        toggle(row, col);
        toggle(row, col + 1);
        toggle(row, col - 1);
    }
    
    var check_if_won = function() {
        var s = 0;
        for (a = 0; a < lights.length; a++) {
            s += lights[a]
        }
        if (s === lights.length) {
            game_won = true;
            $("#win_msg").html("YOU WIN!!");
        }
    }
    set_colors();

    $(".gamepanel").click(function() {
        counter = counter + 1
        id = $(this).attr('id');
        row = parseInt(id[0]);
        col = parseInt(id[1]);
        toggle_neighbors(row, col);
        set_colors();
        check_if_won();
    })

    $("#reset").click(function() {
        counter = 0;
        lights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        game_won = false;
        $("#win_msg").html("Tap to toggle until all lights are out.")
        set_colors();
    })
})