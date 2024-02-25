$(document).ready(function() {
    var lights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
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
        if (row >= 0 && row < 3 && col >= 0 && col < 4) {
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
    })

    $("#reset").click(function() {
        counter = 0;
        lights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        game_won = false;
        set_colors();
    })

    $("#00").click(function() {
        if (game_won === false) {
            toggle_neighbors(0, 0);
            set_colors();
            check_if_won();
        }
    })
    $("#01").click(function() {
        if (game_won === false) {
            toggle_neighbors(0, 1);
            set_colors();
            check_if_won();
        }
    })
    $("#02").click(function() {
        if (game_won === false) {
            toggle_neighbors(0, 2);
            set_colors();
            check_if_won();
        }
    })
    $("#03").click(function() {
        if (game_won === false) {
            toggle_neighbors(0, 3);
            set_colors();
            check_if_won();
        }
    })


    $("#10").click(function() {
        if (game_won === false) {
            toggle_neighbors(1, 0);
            set_colors();
            check_if_won();
        }
    })
    $("#11").click(function() {
        if (game_won === false) {
            toggle_neighbors(1, 1);
            set_colors();
            check_if_won();
        }
    })
    $("#12").click(function() {
        if (game_won === false) {
            toggle_neighbors(1, 2);
            set_colors();
            check_if_won();
        }
    })
    $("#13").click(function() {
        if (game_won === false) {
            toggle_neighbors(1, 3);
            set_colors();
            check_if_won();
        }
    })


    $("#20").click(function() {
        if (game_won === false) {
            toggle_neighbors(2, 0);
            set_colors();
            check_if_won();
        }
    })
    $("#21").click(function() {
        if (game_won === false) {
            toggle_neighbors(2, 1);
            set_colors();
            check_if_won();
        }
    })
    $("#22").click(function() {
        if (game_won === false) {
            toggle_neighbors(2, 2);
            set_colors();
            check_if_won();
        }
    })
    $("#23").click(function() {
        if (game_won === false) {
            toggle_neighbors(2, 3);
            set_colors();
            check_if_won();
        }
    })
})