$(document).ready(function(){
    $('body').on('click', '.word', function(){
        $(this).toggleClass('high');
    });
    $('body').on('click', '#submit', function(){
        var lis = [];
        $('.word.high').each(function(){
            lis[lis.length] = $(this).attr('id').toString();
        });
	console.log("in js clicker");
	console.log(lis.toString());
        $.ajax({
            type: "POST",
            data: {lis : lis.toString()},
            url: "recordAnnotation",
        }).done(function(data){
            data = JSON.parse(data);
            var content = "";
            content += "<h5> Once: " + data.once +  "</h5>";
            content += "<h5> Approved: " + data.approved +  "</h5>";
            content += data.instruction;
            content += data.sentence;
            content += data.buttons;
            $('#holder').html(content);
        });
    });
});
