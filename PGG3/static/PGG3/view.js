function displayValsAdd() {
    var pool = Number($( "#totalPayoff" ).text());
    var totalValue = 0;

    $(".form-control").each(function (index) {
        var currentValue = Number($(this).val());
        totalValue += currentValue;

        if (currentValue != NaN){
            calcPercentage(index, currentValue, pool);
        }
    });

    $(" #currentPayout ").text(totalValue);
}

function displayValsSub() {
    var pool = Number($( "#totalPayoff" ).text());
    var totalValue = pool;

    $(".form-control").each(function (index) {
        var currentValue = $( this ).val();
        totalValue -= Number(currentValue);

        if (currentValue != NaN){
            calcPercentage(index, currentValue, pool);
        }
    });

    $(" #currentPayout ").text(totalValue);
}

function calcPercentage(index, payout, pool) {
    var perc;

    perc = ((payout/pool) * 100).toFixed(2);
    $( ".poolPerc" ).eq(index).text(perc);
}

$('document').ready(function(){
    displayValsSub();
});

//Updates Current distributed amount
//displayValsAdd counts 0 - pool. displayValsSub counts pool - 0
$( ".form-control" ).change( displayValsSub );